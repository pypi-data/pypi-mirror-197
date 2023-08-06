from enum import Enum
from pyquaternion import *
import numpy as np
from scipy.integrate import solve_ivp
import control as ctrl


class ANGLE_UNITS(Enum):
    RADIANS = 0
    DEGREES = 1


def angles_to_quaternion(yaw, pitch, roll, angle_unit=ANGLE_UNITS.DEGREES):
    """
    This function takes the three Euler angles and returns the corresponding
    rotation quaternion as a numpy array.

    :param yaw: yaw angle
    :param pitch: pitch angle
    :param roll: roll angle
    :param angle_unit: units of measurement of the angle
    :returns: quaternion as numpy array
    """
    if angle_unit == ANGLE_UNITS.DEGREES:
        roll = np.deg2rad(roll)
        pitch = np.deg2rad(pitch)
        yaw = np.deg2rad(yaw)

    cphi = np.cos(roll/2)
    ctheta = np.cos(pitch/2)
    cpsi = np.cos(yaw/2)
    sphi = np.sin(roll/2)
    stheta = np.sin(pitch/2)
    spsi = np.sin(yaw/2)
    return np.array([cphi*ctheta*cpsi + sphi*stheta*spsi,
                    sphi*ctheta*cpsi - cphi*stheta*spsi,
                    cphi*stheta*cpsi + sphi*ctheta*spsi,
                    cphi*ctheta*spsi - sphi*stheta*cpsi], dtype=np.float64)


def angles_from_quaterion(q):
    """
    This function takes the state, x, of the quadcopter and returns the three
    Euler angles, φ, θ and ψ, in an numpy array. 
    The Euler angles are in degrees.

    :param x: state vector (numpy array)
    :returns: Euler angles (numpy array): [yaw, pitch, roll]
    """
    w, x, y, z = q[0], q[1], q[2], q[3]
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = np.arctan2(sinr_cosp, cosr_cosp)
    sinp = np.sqrt(1 + 2 * (w * y - x * z))
    cosp = np.sqrt(1 - 2 * (w * y - x * z))
    pitch = 2 * np.arctan2(sinp, cosp) - np.pi / 2
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = np.arctan2(siny_cosp, cosy_cosp)

    return np.rad2deg([yaw, pitch, roll])


class Quadcopter:
    """
    Dynamical model of a quadcopter

    ## Example

    >>> import quadx88 as qx
    >>> copter = qx.Quadcopter(mass=1.15, 
    >>>                        ts=0.0083,
    >>>                        prop_mass=0.01)
    >>> copter.move([0, 0, 0.1])
    >>> print(copter.state)
    """

    def __init__(self, **kwargs):
        """
        Construct a dynamical model for a quadcopter and

        :param ts: sampling time in s (default: 1/125)
        :param m: total quadcopter mass in kg (default: 1)
        :param arm_length: arm length in m (default: 0.225)
        :param moi_xx: x-x moment of inertia (default: 0.01788)
        :param moi_yy: y-y moment of inertia (default: 0.03014)
        :param moi_zz: z-z moment of inertia (default: 0.04614)
        :param gravity_acc: gravitational acceleration in m/s2 (default: 9.81)
        :param air_density: air density in kg/m3 (default: 1.225)
        :param K_v: Kv constant of motors (default: 1000)
        :param motor_time_constant: motor time constant in s (default 0.05)
        :param rotor_mass: rotor mass in kg (default: 0.04)
        :param rotor_radius: rotor radius in m (0.019)
        :param motor_mass: motor mass in kg (default 0.112)
        :param voltage_max: maximum voltage in V (default: 16.8)
        :param voltage_min: minimum voltage in V (default: 15.0)
        :param thrust_coeff: thrust coefficient of propellers (default: 0.112)
        :param power_coeff: power coefficient of propellers (default: 0.044)
        :param prop_mass: propeller mass in kg (default: 0.009)
        :param prop_diameter_in: propeller diameter in inches (default: 10)
        """
        # system state [q0, q1, q2, q3, wx, wy, wz, nx, ny, nz]
        self.__state = np.array([1] + [0] * 9, dtype=np.float64)

        # general
        self.__mass = 1  # kg                               # total mass of aircraft
        self.__arm_length = 0.225  # m                      # quad arm length
        self.__num_motors = 4  # motors                     # no. of motors
        self.__moi_xx = 0.01788  # kg.m^2                   # moment of inertia xx
        self.__moi_yy = 0.03014  # kg.m^2                   # moment of inertia yy
        self.__moi_zz = 0.04614  # kg.m^2                   # moment of inertia zz
        self.__moi = np.diagflat(
            [self.__moi_xx, self.__moi_yy, self.__moi_zz])  # inertia matrix
        self.__gravity_acc = 9.81  # m/s^2                # acceleration of gravity
        self.__air_density = 1.225  # kg/m^3              # air density at sea level, 15 deg C

        # motors
        self.__K_v = 1000  # rpm/V                        # motor speed constant
        self.__motor_time_constant = 50 / 1000  # s       # motor time constant
        self.__rotor_mass = 40 / 1000  # kg               # rotor mass
        self.__rotor_radius = 19 / 1000  # m              # rotor radius
        self.__motor_mass = 112 / 1000  # kg              # total mass of motor
        self.__voltage_max = 16.8  # V                    # max voltage to motor
        self.__voltage_min = 15  # V                      # min voltage to motor

        # props
        self.__thrust_coeff = 0.112  # thrust coefficient
        self.__power_coeff = 0.044  # power coefficient
        self.__prop_mass = 9 / 1000  # kg                 # prop mass
        self.__prop_diameter_in = 10  # prop diameter in inches

        # sampling time
        self.__ts = 1/125

        self.__a_continuous_lin = None
        self.__b_continuous_lin = None
        self.__c_continuous_lin = None
        self.__a_discrete = None
        self.__b_discrete = None
        self.__c_discrete = None

        # parse `kwargs` and set as attribute, provided the keyword corresponds
        # to one of the variables defined above
        for key in kwargs:
            masqueraded_attribute = f"_{self.__class__.__name__}__{key}"
            if masqueraded_attribute in self.__dict__.keys():
                setattr(self, masqueraded_attribute, kwargs[key])
            else:
                raise Exception(f"unknown argument: {key}")

        self.__noise_covariance = self.__ts * \
            np.diagflat([2., 2., 0.5, 1.2, 1.2, 1.2, 2, 2, 2]) / 1e6

        self.__compute_parameters()
        self.__compute_linearisation()
        self.__compute_discretisation()

    def __compute_parameters(self):
        # modelling
        self.__prop_diameter_m = self.__prop_diameter_in * \
            0.0254  # prop diameter in meters
        self.__motor_moi = self.__rotor_mass * (self.__rotor_radius ** 2)
        # kg.m^2           # prop moment of inertia
        self.__prop_moi = (self.__prop_mass * self.__prop_diameter_m ** 2) / 12
        self.__n_h = np.sqrt((self.__mass * self.__gravity_acc) /
                             (self.__num_motors * self.__thrust_coeff
                              * self.__air_density * (self.__prop_diameter_m ** 4)))
        self.__k1 = (self.__K_v * (self.__voltage_max -
                     self.__voltage_min)) / 60  # /60 for rps
        self.__k2 = 1 / self.__motor_time_constant
        self.__k3_x = (2 * self.__n_h * self.__thrust_coeff * self.__air_density * (self.__prop_diameter_m ** 4)
                       * self.__num_motors * self.__arm_length) / ((2 ** 0.5) * self.__moi_xx)
        self.__k3_y = (2 * self.__n_h * self.__thrust_coeff * self.__air_density * (self.__prop_diameter_m ** 4)
                       * self.__num_motors * self.__arm_length) / ((2 ** 0.5) * self.__moi_yy)
        self.__k3_z = (2 * self.__n_h * self.__power_coeff * self.__air_density * (self.__prop_diameter_m ** 5)
                       * self.__num_motors) / (2 * np.pi * self.__moi_zz)
        self.__k4_xy = 0
        self.__k4_z = (2 * np.pi * self.__num_motors *
                       (self.__prop_moi + self.__motor_moi)) / self.__moi_zz
        self.__gamma_n = -np.diagflat(
            [self.__k3_x, self.__k3_y, self.__k3_z - (self.__k4_z * self.__k2)])
        self.__gamma_u = np.diagflat(
            [0, 0, self.__k4_z * self.__k2 * self.__k1])

    @property
    def state(self):
        """
        State of the system, 
        x = (vector part of quaternion, angular velocity, motor spin)
        """
        return self.__state[1:]

    @property
    def quaternion(self):
        """
        Current quaternion of the system 

        See also: euler_angles
        """
        return self.__state[0:4]

    @property
    def hover_rpm(self):
        return self.__n_h

    def set_initial_quaternion(self, q):
        q_array = np.array(q, dtype=np.float64)
        q_norm = np.linalg.norm(q_array)
        self.__state[0:4] = q_array/q_norm

    def set_initial_angular_velocity(self, w):
        self.__state[4:7] = w

    def set_initial_motor_spin(self, spin):
        self.__state[7:10] = spin

    def set_initial_euler_angles(self, yaw, pitch, roll, angle_unit=ANGLE_UNITS.RADIANS):
        self.__state[0:4] = angles_to_quaternion(yaw, pitch, roll, angle_unit)

    def continuous_linearised_matrices(self):
        """
        Dictionary with matrices A, B, and C of the continuous-time linearised dynamics,
        x' = Ax + Bu
        y = Cx
        """
        return {"A": self.__a_continuous_lin,
                "B": self.__b_continuous_lin,
                "C": self.__c_continuous_lin}

    def discrete_linearised_matrices(self):
        """
        Dictionary with matrices A, B, and C of the discrete-time linearised dynamics,
        x+ = Ax + Bu
        y = Cx
        """
        return {"A": self.__a_discrete,
                "B": self.__b_discrete,
                "C": self.__c_discrete}

    def __compute_linearisation(self):
        a = np.zeros(shape=(9, 9))
        b = np.zeros(shape=(9, 3))
        c = np.zeros(shape=(6, 9))
        for i in range(3):
            a[i, 3 + i] = 0.5
            a[3 + i, 6 + i] = self.__gamma_n[i, i]
            a[6 + i, 6 + i] = -self.__k2
            b[3 + i, i] = self.__gamma_u[i, i]
            b[6 + i, i] = self.__k2 * self.__k1

        for i in range(6):
            c[i, i] = 1

        self.__a_continuous_lin = a
        self.__b_continuous_lin = b
        self.__c_continuous_lin = c

    def __compute_discretisation(self):
        continuous_system = ctrl.ss(self.__a_continuous_lin,
                                    self.__b_continuous_lin,
                                    self.__c_continuous_lin, 0)
        discrete_system = ctrl.c2d(continuous_system, self.__ts)
        self.__a_discrete = discrete_system.A
        self.__b_discrete = discrete_system.B
        self.__c_discrete = discrete_system.C

    def euler_angles(self):
        """
        Returns the Euler angles that correspond to the current state 
        of the system 
        """
        q = self.quaternion
        return angles_from_quaterion(q)

    def move(self, u):
        """
        Updates the system state following the application of a given control action 
        for the duration of the sampling time 

        :param u: control action (3-list)
        """
        def dynamics(_t, state):
            control_action = np.asarray(u).reshape(3, )  # control input
            attitude_quat = Quaternion(state[0:4])  # attitude as a quaternion
            angular_freq = state[4:7]  # angular frequencies
            rotor_freq = state[7:10]  # rotor frequencies
            angular_freq_quat = Quaternion(np.append(0, angular_freq))
            attitude_quat_dot = list(0.5 * attitude_quat * angular_freq_quat)
            # af = angular_freq  # flatten 3x3 array to 1x3
            af1 = np.diag(self.__moi * angular_freq)
            angular_freq_cross = np.cross(angular_freq, af1)
            angular_freq_dot = list(np.diag(self.__gamma_n * rotor_freq + self.__gamma_u * control_action
                                            - np.diagflat(1 / np.diag(self.__moi)) * angular_freq_cross))
            rotor_freq_dot = list(
                self.__k2 * (self.__k1 * control_action - rotor_freq))
            return attitude_quat_dot + angular_freq_dot + rotor_freq_dot

        solution = solve_ivp(dynamics, [0, self.__ts], self.__state)
        self.__state = solution.y[:, -1]

        w = np.random.multivariate_normal(
            np.zeros((9, )), self.__noise_covariance)
        self.__state[1:] += w

        norm = Quaternion(self.__state[0:4]).norm
        self.__state[0:4] = self.__state[0:4] / norm

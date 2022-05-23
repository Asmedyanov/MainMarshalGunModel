"""Модель серии экспериментов с изменяемым напряжением"""
from classes.ShotClass import Shot
import numpy as np
import matplotlib.pyplot as plt

R_gas = 8.31
"""Газовая постоянная"""
aem = 1.7e-27
"""Атомная единица массы"""
N_Avagadro = 6.02e23
"""Число Авагадро"""


class Volt_mod:
    def __init__(self, *args, **kwargs):
        try:
            self.init_full(*args, **kwargs)
        except:
            self.init_default()

    def init_full(self, *args, **kwargs):
        """Полная инициализация"""
        self.mCapacity = kwargs['Capacity']
        self.mU0_min = kwargs['U0_min']
        self.mU0_max = kwargs['U0_max']
        self.mU0_step = kwargs['U0_step']
        self.mL0 = kwargs['L0']
        self.mD_in = kwargs['D_in']
        self.mD_out = kwargs['D_out']
        self.mGun_length = kwargs['Gun_length']
        self.mV_valve = kwargs['V_valve']
        self.mP_valve = kwargs['P_valve']
        self.mPart = kwargs['Part']
        self.mT_gas = kwargs['T_gas']
        self.mTime_step = kwargs['Time_step']
        self.mTime_length = kwargs['Time_length']
        self.prepare_data()
        self.find_solution()

    def init_default(self):
        """Инициализация по умолчанию"""
        self.mCapacity = 560.0e-6
        self.mU0_min = 0.8e3
        self.mU0_max = 6.0e3
        self.mU0_step = 0.05e3
        self.mL0 = 270.0e-9
        self.mD_in = 10.0e-3
        self.mD_out = 40.0e-3
        self.mV_valve = 1.0e-6
        self.mP_valve = 1.0e5
        self.mPart = 2.0
        self.mT_gas = 300.0
        self.mTime_step = 1.0e-8
        self.mTime_length = 100.0e-6
        self.mGun_length = 0.8
        self.prepare_data()
        self.find_solution()

    def prepare_data(self):
        self.mU0 = np.arange(self.mU0_min, self.mU0_max, self.mU0_step)

    def find_solution(self):
        Voltage = []
        Current = []
        Speed = []
        for U0 in self.mU0:
            shot = Shot(
                Capacity=self.mCapacity,
                U0=U0,
                L0=self.mL0,
                D_in=self.mD_in,
                D_out=self.mD_out,
                Gun_length=self.mGun_length,
                V_valve=self.mV_valve,
                P_valve=self.mP_valve,
                Part=self.mPart,
                T_gas=self.mT_gas,
                Time_step=self.mTime_step,
                Time_length=self.mTime_length
            )
            #shot.plot()

            Exit_index = np.min(np.nonzero(shot.mCoordinat > self.mGun_length))
            Current.append(shot.mCurrent[Exit_index])
            Voltage.append(shot.mVoltage[Exit_index])
            Speed.append(shot.mSpeed[Exit_index])
        self.mVoltage = np.array(Voltage)
        self.mCurrent = np.array(Current)
        self.mSpeed = np.array(Speed)
        self.mNu_gas = self.mP_valve * self.mV_valve / (self.mT_gas * R_gas)
        self.mM_gas = self.mPart * self.mNu_gas * 1.0e-3
        self.mEnergy = self.mM_gas * np.square(self.mSpeed) / 2.0
        self.mE0 = self.mCapacity * np.square(self.mU0) / 2.0
        self.mKPD = 100.0 * self.mEnergy / self.mE0

    def plot(self):

        plt.subplot(3, 1, 1)
        plt.plot(self.mU0 * 1.0e-3, self.mSpeed * 1.0e-3)
        plt.xlabel("Напряжение, кВ")
        plt.ylabel("Скорость, км/с")
        plt.grid()

        plt.subplot(3, 1, 2)
        plt.plot(self.mU0 * 1.0e-3, self.mEnergy)
        plt.xlabel("Напряжение, кВ")
        plt.ylabel("Энергия, Дж")
        plt.grid()

        plt.subplot(3, 1, 3)
        plt.plot(self.mU0 * 1.0e-3, self.mKPD)
        plt.xlabel("Напряжение, кВ")
        plt.ylabel("КПД, %")
        plt.grid()

        plt.show()

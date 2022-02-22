from pandas import DataFrame
import

Rgas = 8.31
aem = 1.7e-27


class Shot(DataFrame):
    def __init__(self):
        super().__init__()
        self.mCapacity = 560.0e-6
        self.mU0 = 2.0e3
        self.mL0 = 270.0e-9
        self.mDin = 10.0e-3
        self.mDout = 40.0e-3
        self.mVvalve = 1.0e-6
        self.mPvalve = 1.0e5
        self.mAtom = 2.0 * aem
        self.mTgas = 300.0
        self.mDt = 1.0e-7
        self.mLt = 100.0e-6

        self.mNu = self.mPvalve * self.mVvalve / (self.mTgas * Rgas)
        self.mMgas = self.mAtom * self.mNu
        self.mT0
        self.mW0 = 1.0/

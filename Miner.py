from py_stealth import *
from RunebookHandler import Runebook
from datetime import datetime
from scipy import spatial


class Miner:
    def __init__(self, _homeRuneBookName, _miningBookNames, _storage):
        SetEventProc('evSpeech', self.OnSpeech)
        self._diggingTools = []
        self._tinkerTools = []
        self._storage = _storage
        self._runebookHome = Runebook(_homeRuneBookName, "recall", "osi")
        self._runebooksMining = []
        for _miningBook in _miningBookNames:
            self._runebooksMining.append(Runebook(_miningBook, "recall", "osi"))
        self._messageFail = "You loosen some rocks| You dig some "
        self._messageEnd = "There is nothing here |" \
                           "There is no metal |" \
                           "You cannot mine |" \
                           "You have no line |" \
                           "That is too far |" \
                           "Try mining elsewhere |" \
                           "You can't mine |" \
                           "someone |" \
                           "Target cannot be"
        self._messageAttack = "is attacking you"
        self._messageAll = self._messageFail + "|" + self._messageEnd + "|" + self._messageAttack
        self._oreTypes = ['0x19b9',  # large
                          '0x19ba',  # medium
                          '0x19b8',  # medium2
                          '0x19b7']  # small
        self._oreColors = ['0x0',  # Iron
                           '0x973',  # Dull Copper
                           '0x966',  # Shadow Iron
                           '0x96D',  # Copper
                           '0x972',  # Bronze
                           '0x8A5',  # Golden
                           '0x979',  # Agapite
                           '0x89F',  # Verite
                           '0x8AB']  # Valorite
        self._minableTypes = [220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 236, 237, 238, 239, 240, 241,
                              242, 243, 244, 245, 246, 247, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263,
                              268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 286, 287, 288, 289, 290, 291,
                              292, 293, 294, 296, 296, 297, 321, 322, 323, 324, 467, 468, 469, 470, 471, 472, 473, 474,
                              476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 492, 493, 494, 495, 543, 544,
                              545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562,
                              563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 581,
                              582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599,
                              600, 601, 610, 611, 612, 613, 1010, 1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347,
                              1348, 1349, 1350, 1351, 1352, 1353, 1354, 1355, 1356, 1357, 1358, 1359, 1361, 1362, 1363,
                              1386, 1741, 1742, 1743, 1744, 1745, 1746, 1747, 1748, 1749, 1750, 1751, 1752, 1753, 1754,
                              1755, 1756, 1757, 1771, 1772, 1773, 1774, 1775, 1776, 1777, 1778, 1779, 1780, 1781, 1782,
                              1783, 1784, 1785, 1786, 1787, 1788, 1789, 1790, 1801, 1802, 1803, 1804, 1805, 1806, 1807,
                              1808, 1809, 1811, 1812, 1813, 1814, 1815, 1816, 1817, 1818, 1819, 1820, 1821, 1822, 1823,
                              1824, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1839, 1840, 1841, 1842, 1843, 1844,
                              1845, 1846, 1847, 1848, 1849, 1850, 1851, 1852, 1853, 1854, 1861, 1862, 1863, 1864, 1865,
                              1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880,
                              1881, 1882, 1883, 1884, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991,
                              1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2028, 2029,
                              2030, 2031, 2032, 2033, 2100, 2101, 2102, 2103, 2104, 2105, 0x453B, 0x453C, 0x453D,
                              0x453E, 0x453F, 0x4540, 0x4541, 0x4542, 0x4543, 0x4544, 0x4545, 0x4546, 0x4547, 0x4548,
                              0x4549, 0x454A, 0x454B, 0x454C, 0x454D, 0x454E, 0x454F]

    @property
    def RunebooksMining(self):
        return self._runebooksMining

    @property
    def DiggingTools(self):
        if FindTypesArrayEx([0xE86, 0xE85, 0xF39], [0xFFFF], [Backpack()], False):
            self._diggingTools = GetFindedList()
            self._diggingTools = list(dict.fromkeys(self._diggingTools))
            return self._diggingTools
        else:
            return 0

    @property
    def TinkerTools(self):
        if FindTypesArrayEx([0x1EB8, 0x1EB9], [0xFFFF], [Backpack()], False):
            self._tinkerTools = GetFindedList()
            self._tinkerTools = list(dict.fromkeys(self._diggingTools))
            return self._tinkerTools
        else:
            return 0

    @property
    def Mounted(self):
        return ObjAtLayerEx(HorseLayer(), Self())

    def MakeTools(self):
        AddToSystemJournal("Making tools...")
        if self.TinkerTools:
            while len(self.TinkerTools) <= 5:
                UseObject(self.TinkerTools[0])
                Wait(250)
                WaitGump('23')
                Wait(1500)
        else:
            AddToSystemJournal("No tinker tools found, forced to stop.")
            exit()
        Wait(1000)
        while True:
            UseObject(self.TinkerTools[0])
            Wait(250)
            WaitGump('114')
            Wait(250)
            WaitGump('0')
            Wait(1500)
            if self.DiggingTools > 10:
                break

    def DropoffOre(self):
        AddToSystemJournal("Dropping off ore...")
        self._runebookHome.Recall(1)
        newMoveXY(GetX(self._storage), GetY(self._storage), True, 1, True)
        UseObject(self._storage)
        for _oreColor in self._oreColors:
            for _oreType in self._oreTypes:
                if FindTypesArrayEx([_oreType], [_oreColor], Backpack(), False):
                    _oreList = GetFindedList()
                    for _ore in _oreList:
                        MoveItem(_ore, GetQuantity(_ore), self._storage, 0, 0, 0)
                        Wait(750)

    def Mine(self, _radius):
        _mining = True
        _startTime = datetime.now()
        while Weight() < (MaxWeight() - 20) and _mining:
            if not self.DiggingTools:
                AddToJournal("no digging tools found")
                self.MakeTools()
            _minableTiles = GetLandTilesArray(GetX(Self()) - _radius, GetY(Self()) - _radius,
                                              GetX(Self()) + _radius, GetY(Self()) + _radius,
                                              WorldNum(), self._minableTypes)
            _minableCoords = []
            for _tile in _minableTiles:
                _minableCoords.append(tuple((_tile[1], _tile[2])))
            _tree = spatial.KDTree(_minableCoords)
            _query = _tree.query([GetX(Self()), GetY(Self())])  # find next closest coords
            _key = _query[1]
            newMoveXYZ(_minableTiles[_key][1], _minableTiles[_key][2], _minableTiles[_key][3], True, 0, True)
            while _mining:
                if Weight() >= (MaxWeight() - 20) or self.DiggingTools == 0:
                    _mining = False
                    break
                UseObject(self.DiggingTools[0])
                WaitForTarget(500)
                TargetToTile(_minableTiles[_key][0], _minableTiles[_key][1],
                             _minableTiles[_key][2], _minableTiles[_key][3])
                WaitJournalLine(_startTime, self._messageAll, 120000)
                if (InJournalBetweenTimes(self._messageEnd, _startTime, datetime.now())) > 0:
                    _mining = False
                    break
        return

    def OnSpeech(self, _text, _senderName, _senderID):
        return

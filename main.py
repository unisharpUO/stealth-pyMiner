from py_stealth import *
from Miner import Miner


def Reconnect():
    while not Connected():
        Connect()
        Wait(10000)


if __name__ == "__main__":
    AddToSystemJournal("stealth-pyMiner script starting...")

    AddToSystemJournal("Target your storage container...")
    _storage = ClientRequestObjectTarget()

    #  Miner(homerunebook name, [mining book names], storage container)
    _m = Miner("Home", ["Mining1", "Mining2"], _storage)

    while _m.Mounted:
        UseObject(Self())
        Wait(750)

    _m.DropoffOre()

    while not Dead():
        if not _m.DiggingTools:
            _m.MakeTools()

        for _miningBook in _m.RunebooksMining:
            for _rune in range(0, 15):
                _miningBook.Recall(_rune)
                _m.Mine(10)
                if Weight() >= (MaxWeight() - 20):
                    _m.DropoffOre()
                if not _m.DiggingTools:
                    _m.MakeTools()

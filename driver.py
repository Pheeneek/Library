import json


class IStructureDriver:
    def read(self):
        pass

    def write(self, d):
        pass


class JsonFileDriver(IStructureDriver):
    def __init__(self, filename):
        self.filename = filename

    def read(self) -> list:
        with open(self.filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write(self, d) -> None:
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(d, f)


class MyList:
    def __init__(self, list_=None, driver: IStructureDriver = None):
        self.driver = driver

        if list_ is None:
            if driver is None:
                self.__list = []
            else:
                self.__list = self.driver.read()
        else:
            self.__list = list_

    def __str__(self):
        return str(self.__list)

    def write(self):
        self.driver.write(self.__list)

    def read(self):
        self.__list = self.driver.read()


if __name__ == '__main__':
    json_driver = JsonFileDriver('test')
    l = MyList([1, 2, 3], driver=json_driver)

    print(l)

    l1 = MyList(driver=json_driver)
    print(l1)

    l2 = MyList()
    print(l2)

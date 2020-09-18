from driver import JsonFileDriver


class DriverBuilder:
    def build(self):
        return None


class JsonFileBuilder(DriverBuilder):
    def build(self):
        while True:
            filename = input('Введите название json файла: (.json)')
            filename = filename.strip()
            if not filename.endswith('.json'):
                print('Файл должен оканчиваться на .json')
                continue
            break

        return JsonFileDriver(filename)


class FabricDriverBuilder:
    @staticmethod
    def get_driver():
        driver_name = input("Введите название драйвера: ")

        drivers = {
            'json_file': JsonFileBuilder
        }

        return drivers[driver_name]().build()


if __name__ == '__main__':
    driver = FabricDriverBuilder.get_driver()

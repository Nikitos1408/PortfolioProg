class Component():
    """
    Базовый интерфейс Компонента определяет поведение, которое изменяется
    декораторами.
    """

    def operation(self) -> str:
        pass


class ConcreteComponent(Component):
    """
    Конкретные Компоненты предоставляют реализации поведения по умолчанию. Может
    быть несколько вариаций этих классов.
    Для нашей программы ConcreteComponent - Класс возвращающий dict
    """

    def operation(self) -> str:
        return "ConcreteComponent"


class Decorator(Component):
    """
    Базовый класс Декоратора следует тому же интерфейсу, что и другие
    компоненты. Основная цель этого класса - определить интерфейс обёртки для
    всех конкретных декораторов. Реализация кода обёртки по умолчанию может
    включать в себя поле для хранения завёрнутого компонента и средства его
    инициализации.
    """

    _component: Component = None

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> str:
        """
        Декоратор делегирует всю работу обёрнутому компоненту.
        """

        return self._component

    def operation(self) -> str:
        return self._component.operation()


class ConcreteDecoratorA(Decorator):
    """
    Конкретные Декораторы вызывают обёрнутый объект и изменяют его результат
    некоторым образом.
    Для нашей программы ConcreteDecoratorA - Класс возвращающий json
    """

    def operation(self) -> str:
        """
        Декораторы могут вызывать родительскую реализацию операции, вместо того,
        чтобы вызвать обёрнутый объект напрямую. Такой подход упрощает
        расширение классов декораторов.
        """
        return f"ConcreteDecoratorA({self.component.operation()})"


class ConcreteDecoratorB(Decorator):
    """
    Декораторы могут выполнять своё поведение до или после вызова обёрнутого
    объекта.
    Для нашей программы ConcreteDecoratorA - Класс возвращающий csv
    """

    def operation(self) -> str:
        return f"ConcreteDecoratorB({self.component.operation()})"


def client_code(component: Component) -> None:
    """
    Клиентский код работает со всеми объектами, используя интерфейс Компонента.
    Таким образом, он остаётся независимым от конкретных классов компонентов, с
    которыми работает.
    """

    # ...

    print(f"RESULT: {component.operation()}", end="")

    # ...


# Таким образом, клиентский код может поддерживать как простые компоненты...
simple = ConcreteComponent()
print("Client: I've got a simple component:")
client_code(simple)
print("\n")

# # ...так и декорированные.
# #
# # Обратите внимание, что декораторы могут обёртывать не только простые
# # компоненты, но и другие декораторы.
decorator1 = ConcreteDecoratorA(simple)
decorator2 = ConcreteDecoratorB(decorator1)

print("Client: Now I've got a decorated component:")
# client_code(decorator1)
client_code(decorator2)

# class A():
#     def __init__(self, d):
#         self.d = d

#     def __repr__(self):
#         return f"{type(self.d)} with {tuple(self.d.keys())} and {tuple(self.d.values())}"

#     def __str__(self):
#         return f"{list(self.d.keys())[0]}: {self.d['k']}"

# if __name__ == "__main__":

#     a = A({'k': 100500})

#     a
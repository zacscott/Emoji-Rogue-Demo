import engine.gfx


class EntityType:
    """
    Base entity type class which should be extended for each of the games entities.
    Child classes should override update() for each entity type.
    """

    def __init__(self, char, fg, bg):
        """

        :param char: Character displayed for the entity
        :param fg: Foreground colour of the entity
        :param bg: Background colour of the entity
        """

        self._char = char
        self._fg = fg
        self._bg = bg


    def update(self, entity):
        """
        Update the given entity instance.
        :param entity: The entity instance to update
        """
        pass


    def render(self, entity):
        """
        Render the given entity to the console.
        :param entity: The entity instance to render
        """

        engine.gfx.fg(self._fg)
        engine.gfx.bg(self._bg)

        engine.gfx.plot(
            self._char,
            entity.x, entity.y
        )


class Entity:
    """Single entity. Will have a single EntityType associated with it."""


    def __init__(self, entity_type):
        """

        :param entty_type: The EntityType for the entity
        """

    def render(self):

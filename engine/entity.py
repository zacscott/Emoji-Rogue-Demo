import engine.gfx


class EntityType:
    """
    Base entity type class which should be extended for each of the games entities.
    Child classes should override update() for each entity type.
    """

    def __init__(self, block):
        """

        :param block: 3 tuple of the block for the entity (char, fg, bg)
        """

        self.block = block
        self.game = None


    def spawn(self, pos):
        """
        Spawn & return a new entity of this type at the given location
        :param pos: 2 tuple of the new entities location on the map
        """

        entity = Entity(self)
        entity.game = self.game
        entity.x, entity.y = pos

        return entity


    def update(self, entity, key):
        """
        Update the given entity instance.
        :param entity: The entity instance to update
        :param key: The key which was pressed to cause the update
        """
        pass


    def render(self, entity, offset):
        """
        Render the given entity to the console.
        :param entity: The entity instance to render
        """

        offset_x, offset_y = offset

        engine.gfx.plot(
            (entity.x - offset_x, entity.y - offset_y),
            self.block
        )


class Entity:
    """Single entity. Will have a single EntityType associated with it."""


    def __init__(self, entity_type):
        """

        :param entity_type: The EntityType for the entity
        """

        self.x, self.y = 0, 0
        self.entity_type = entity_type
        self.game = None


    def update(self, key):
        """Render the entity to the screen"""
        self.entity_type.update(self, key)


    def render(self, offset):
        """Render the entity to the screen"""
        self.entity_type.render(self, offset)

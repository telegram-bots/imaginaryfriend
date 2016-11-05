from orator.migrations import Migration


class CreatePairsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('pairs') as table:
            table.increments('id')
            table.integer('chat_id').unsigned()
            table.foreign('chat_id').references('id').on('chats')
            table.integer('first_id').unsigned().nullable()
            #table.foreign('first_id').references('id').on('replies').nullable()
            table.integer('second_id').unsigned().nullable()
            #table.foreign('second_id').references('id').on('replies').nullable()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('pairs')

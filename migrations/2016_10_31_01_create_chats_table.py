from orator.migrations import Migration


class CreateChatsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('chats') as table:
            table.increments('id')
            table.integer('telegram_id').unique()
            table.string('chat_type')
            table.integer('random_chance').default(5)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('chats')

from orator.migrations import Migration


class CreateRepliesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('replies') as table:
            table.increments('id')
            table.integer('pair_id').unsigned()
            table.foreign('pair_id').references('id').on('pairs')
            table.integer('word_id').unsigned().nullable()
            # table.foreign('word_id').references('id').on('words').nullable()
            table.integer('count').default(1)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('replies')

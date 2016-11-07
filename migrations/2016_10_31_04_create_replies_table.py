from orator.migrations import Migration


class CreateRepliesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('replies') as table:
            table.increments('id')
            table.integer('pair_id')
            table.integer('word_id').nullable()
            table.integer('count').default(1)

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('replies')

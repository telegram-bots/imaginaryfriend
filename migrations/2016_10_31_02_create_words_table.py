from orator.migrations import Migration


class CreateWordsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('words') as table:
            table.increments('id')
            table.string('word').unique()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('words')

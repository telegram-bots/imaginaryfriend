from orator.migrations import Migration


class CreatePairsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('pairs') as table:
            table.increments('id')
            table.integer('chat_id')
            table.integer('first_id').nullable()
            table.integer('second_id').nullable()
            # table.unique(
            #     ['chat_id', 'first_id', 'second_id'],
            #     name='unique_pairs_idx'
            # )
            table.timestamp('created_at').default('CURRENT_TIMESTAMP')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('pairs')

from orator.migrations import Migration


class CreateJobsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('jobs') as table:
            table.increments('id')
            table.integer('chat_id')
            table.string('type')
            table.boolean('repeat')
            table.timestamp('execute_at')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('jobs')

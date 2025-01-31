class AppDatabaseRouter:
    """Routes database operations to different SQLite databases based on the app."""

    app_labels = {
        'myApps.auction': 'auction_db',  # Directs the "auction" app to use "auction_db"
    }

    def db_for_read(self, model, **hints):
        """Point read operations to the correct database."""
        return self.app_labels.get(model._meta.app_label, 'default')

    def db_for_write(self, model, **hints):
        """Point write operations to the correct database."""
        return self.app_labels.get(model._meta.app_label, 'default')

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relationships within the same database."""
        db_set = {self.db_for_read(obj1), self.db_for_read(obj2)}
        return len(db_set) == 1 or 'default' in db_set

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure migrations are applied to the correct database."""
        return self.app_labels.get(app_label, 'default') == db

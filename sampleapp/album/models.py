from django.db import models


class Album(models.Model):
    """Album model to keep the album record."""

    original_img = models.ImageField(blank=True, null=True, upload_to="originalimg")
    compress_img = models.ImageField(blank=True, null=True, upload_to="compressimg")
    created_at = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """Return string representation of object."""
        return self.created_at

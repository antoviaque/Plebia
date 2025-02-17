# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Post.episode'
        db.delete_column('wall_post', 'episode_id')

        # Adding field 'Post.series'
        db.add_column('wall_post', 'series', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['wall.Series']), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'Post.episode'
        raise RuntimeError("Cannot reverse this migration. 'Post.episode' and its values cannot be restored.")

        # Deleting field 'Post.series'
        db.delete_column('wall_post', 'series_id')


    models = {
        'wall.post': {
            'Meta': {'object_name': 'Post'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wall.Series']"})
        },
        'wall.series': {
            'Meta': {'object_name': 'Series'},
            'banner_url': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_aired': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'overview': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'tvdb_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'wall.seriesseason': {
            'Meta': {'object_name': 'SeriesSeason'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wall.Series']"}),
            'torrent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wall.Torrent']", 'null': 'True'})
        },
        'wall.seriesseasonepisode': {
            'Meta': {'object_name': 'SeriesSeasonEpisode'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'next_episode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wall.SeriesSeasonEpisode']", 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wall.SeriesSeason']"}),
            'torrent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wall.Torrent']", 'null': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wall.Video']", 'null': 'True', 'blank': 'True'})
        },
        'wall.torrent': {
            'Meta': {'object_name': 'Torrent'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'download_speed': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'eta': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'peers': ('django.db.models.fields.IntegerField', [], {}),
            'progress': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'seeds': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'New'", 'max_length': '20'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'upload_speed': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'wall.video': {
            'Meta': {'object_name': 'Video'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'mp4_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'ogv_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'original_path': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'New'", 'max_length': '20'}),
            'webm_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['wall']

# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShareZone'
        db.create_table('Sharing_sharezone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('Sharing', ['ShareZone'])

        # Adding model 'Shed'
        db.create_table('Sharing_shed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('sharezone', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sheds', blank=True, null=True, to=orm['Sharing.ShareZone'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('Sharing', ['Shed'])

        # Adding model 'Coordinator'
        db.create_table('Sharing_coordinator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['UserAuth.UserProfile'], unique=True)),
            ('shed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sharing.Shed'], unique=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('Sharing', ['Coordinator'])

        # Adding model 'Arrangement'
        db.create_table('Sharing_arrangement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('pickup_arrangement', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('borrower', self.gf('django.db.models.fields.related.ForeignKey')(related_name='borrowers', to=orm['UserAuth.UserProfile'])),
            ('lender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lenders', to=orm['UserAuth.UserProfile'])),
        ))
        db.send_create_signal('Sharing', ['Arrangement'])

        # Adding model 'Sharing'
        db.create_table('Sharing_sharing', (
            ('arrangement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Sharing.Arrangement'], primary_key=True, unique=True)),
        ))
        db.send_create_signal('Sharing', ['Sharing'])

        # Adding model 'Request'
        db.create_table('Sharing_request', (
            ('arrangement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Sharing.Arrangement'], primary_key=True, unique=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('Sharing', ['Request'])


    def backwards(self, orm):
        # Deleting model 'ShareZone'
        db.delete_table('Sharing_sharezone')

        # Deleting model 'Shed'
        db.delete_table('Sharing_shed')

        # Deleting model 'Coordinator'
        db.delete_table('Sharing_coordinator')

        # Deleting model 'Arrangement'
        db.delete_table('Sharing_arrangement')

        # Deleting model 'Sharing'
        db.delete_table('Sharing_sharing')

        # Deleting model 'Request'
        db.delete_table('Sharing_request')


    models = {
        'Sharing.arrangement': {
            'Meta': {'object_name': 'Arrangement'},
            'borrower': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'borrowers'", 'to': "orm['UserAuth.UserProfile']"}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lenders'", 'to': "orm['UserAuth.UserProfile']"}),
            'pickup_arrangement': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'request_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'Sharing.coordinator': {
            'Meta': {'object_name': 'Coordinator'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Sharing.Shed']", 'unique': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['UserAuth.UserProfile']", 'unique': 'True'})
        },
        'Sharing.request': {
            'Meta': {'object_name': 'Request', '_ormbases': ['Sharing.Arrangement']},
            'approved': ('django.db.models.fields.BooleanField', [], {}),
            'arrangement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Sharing.Arrangement']", 'primary_key': 'True', 'unique': 'True'})
        },
        'Sharing.sharezone': {
            'Meta': {'object_name': 'ShareZone'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {})
        },
        'Sharing.sharing': {
            'Meta': {'object_name': 'Sharing', '_ormbases': ['Sharing.Arrangement']},
            'arrangement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Sharing.Arrangement']", 'primary_key': 'True', 'unique': 'True'})
        },
        'Sharing.shed': {
            'Meta': {'object_name': 'Shed'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sharezone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sheds'", 'blank': 'True', 'null': 'True', 'to': "orm['Sharing.ShareZone']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'UserAuth.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'add_line1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'add_line2': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pickup_loc': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'profile_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'reminder_preferences': ('django.db.models.fields.IntegerField', [], {}),
            'sharezone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'members'", 'blank': 'True', 'null': 'True', 'to': "orm['Sharing.ShareZone']"}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'related_name': "'profile'", 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Sharing']
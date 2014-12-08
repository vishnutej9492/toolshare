# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Sharing.rated'
        db.add_column('Sharing_sharing', 'rated',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Sharing.sharing_comment'
        db.add_column('Sharing_sharing', 'sharing_comment',
                      self.gf('django.db.models.fields.CharField')(null=True, max_length=200, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Sharing.rated'
        db.delete_column('Sharing_sharing', 'rated')

        # Deleting field 'Sharing.sharing_comment'
        db.delete_column('Sharing_sharing', 'sharing_comment')


    models = {
        'Sharing.arrangement': {
            'Meta': {'object_name': 'Arrangement'},
            'borrower': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'asked_requests'", 'to': "orm['UserAuth.UserProfile']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recieved_requests'", 'to': "orm['UserAuth.UserProfile']"}),
            'pickup_arrangement': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'tool': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'tools'", 'to': "orm['ToolMgmt.Tool']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'Sharing.request': {
            'Meta': {'_ormbases': ['Sharing.Arrangement'], 'object_name': 'Request'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'arrangement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['Sharing.Arrangement']", 'primary_key': 'True'}),
            'msg': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sharing': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'related_name': "'request'", 'to': "orm['Sharing.Sharing']", 'unique': 'True', 'blank': 'True'})
        },
        'Sharing.sharezone': {
            'Meta': {'object_name': 'ShareZone'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {})
        },
        'Sharing.sharing': {
            'Meta': {'_ormbases': ['Sharing.Arrangement'], 'object_name': 'Sharing'},
            'arrangement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['Sharing.Arrangement']", 'primary_key': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rated': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'returned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sharing_comment': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'})
        },
        'Sharing.shed': {
            'Meta': {'object_name': 'Shed'},
            'coordinators': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'sheds'", 'to': "orm['UserAuth.UserProfile']", 'symmetrical': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sharezone': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'sheds'", 'to': "orm['Sharing.ShareZone']", 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ToolMgmt.tool': {
            'Meta': {'object_name': 'Tool'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'category'", 'to': "orm['ToolMgmt.ToolCategory']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'in_shed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'owner'", 'to': "orm['UserAuth.UserProfile']"}),
            'shed': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'tools'", 'to': "orm['Sharing.Shed']", 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'status'", 'to': "orm['ToolMgmt.ToolStatus']"})
        },
        'ToolMgmt.toolcategory': {
            'Meta': {'object_name': 'ToolCategory'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ToolMgmt.toolstatus': {
            'Meta': {'object_name': 'ToolStatus'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'UserAuth.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'add_line1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'add_line2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pickup_loc': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'profile_photo': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'reminder_preferences': ('django.db.models.fields.IntegerField', [], {}),
            'sharezone': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'members'", 'to': "orm['Sharing.ShareZone']", 'blank': 'True'}),
            'state': ('localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'to': "orm['auth.User']", 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Sharing']
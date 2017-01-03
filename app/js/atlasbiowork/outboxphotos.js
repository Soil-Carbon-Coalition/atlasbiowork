define({
    'context': function(context, routeInfo) {
        if (routeInfo.page != 'observation') {
            return {};
        } else if (routeInfo.mode == 'list') {
            return this.listContext();
        } else if (routeInfo.mode == 'edit') {
            return this.editContext(context);
        }
    },
    'listContext': function() {
        return {
            'default_photo': function() {
                var data = this, photo;
                Object.keys(data).forEach(function(key) {
                    if (data[key] && data[key].body && data[key].type) {
                        photo = data[key];
                    }
                });
                return photo;
            }
        };
    },
    'editContext': function(context) {
        if (!(context.outbox_id && context.type && context.type.form_json)) {
            return {};
        }
        var fields = context.type.form_json.children,
            preserve = [];
        fields.forEach(function(field) {
            if (field.type == 'photo') {
                preserve.push(field.name);
            } else if (field.children) {
                field.children.forEach(function(cfield) {
                    if (cfield.type != 'photo') {
                        return;
                    }
                    if (field.type == 'group') {
                         preserve.push(field.name + '[' + cfield.name + ']');
                    } else {
                         (context[field.name] || []).forEach(function(row, i) {
                             preserve.push(
                                 field.name + '[' + i + '][' + cfield.name + ']'
                             );
                         });
                    }
                });
            }
        });
        return {
            'file_fields': preserve.join(',')
        };
    }
});

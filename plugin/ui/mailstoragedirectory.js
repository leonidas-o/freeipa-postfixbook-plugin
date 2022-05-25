define([
    'freeipa/phases',
    'freeipa/ipa'],
    function(phases, IPA) {
    
    // helper function
    function get_item(array, attr, value) {
    for (var i=0,l=array.length; i<l; i++) {
        if (array[i][attr] === value) 
            return array[i];
        }
        return null;
    }

    var mail_storage_directory_plugin = {};

    // adds 'mailstoragedirectory' field into user details facet
    mail_storage_directory_plugin.add_mail_storage_directory_pre_op = function() {
        var facet = get_item(IPA.user.entity_spec.facets, '$type', 'details');
        var section = get_item(facet.sections, 'name', 'misc');
        section.fields.push({
            $type: 'text', 
            name: 'mailstoragedirectory', 
            flags: ['w_if_no_aci'],
            options: [
                { label: 'Mail storage directory' }
            ],
            tooltip: {
                title: 'The absolute path to the mail users mailbox',
                html: true
            },
        });
        return true;	
    };

    phases.on('customization', mail_storage_directory_plugin.add_mail_storage_directory_pre_op);

    return mail_storage_directory_plugin;
});
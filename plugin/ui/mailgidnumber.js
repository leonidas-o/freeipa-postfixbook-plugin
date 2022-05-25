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

    var mail_gid_number_plugin = {};

    // adds 'mailgidnumber' field into user details facet
    mail_gid_number_plugin.add_mail_gid_number_pre_op = function() {
        var facet = get_item(IPA.user.entity_spec.facets, '$type', 'details');
        var section = get_item(facet.sections, 'name', 'misc');
        section.fields.push({
            $type: 'text', 
            name: 'mailgidnumber', 
            flags: ['w_if_no_aci'],
            options: [
                { label: 'Mail GID number' }
            ],
            tooltip: {
                title: 'GID required to access the mailbox',
                html: true
            },
        });
        return true;	
    };

    phases.on('customization', mail_gid_number_plugin.add_mail_gid_number_pre_op);

    return mail_gid_number_plugin;
});
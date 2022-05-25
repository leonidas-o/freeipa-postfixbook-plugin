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

    var mail_group_member_plugin = {};

    // adds 'mailgroupmember' field into user details facet
    mail_group_member_plugin.add_mail_group_member_pre_op = function() {
        var facet = get_item(IPA.user.entity_spec.facets, '$type', 'details');
        var section = get_item(facet.sections, 'name', 'misc');
        section.fields.push({
            $type: 'multivalued', 
            name: 'mailgroupmember', 
            flags: ['w_if_no_aci'],
            options: [
                { label: 'Mail group member' }
            ],
            tooltip: {
                title: 'Name of a mail distribution list',
                html: true
            },
        });
        return true;	
    };

    phases.on('customization', mail_group_member_plugin.add_mail_group_member_pre_op);

    return mail_group_member_plugin;
});
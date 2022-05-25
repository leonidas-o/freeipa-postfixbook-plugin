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

    var mail_enabled_plugin = {};

    // adds 'mailenabled' field into user details facet
    mail_enabled_plugin.add_mail_enabled_pre_op = function() {
        var facet = get_item(IPA.user.entity_spec.facets, '$type', 'details');
        var section = get_item(facet.sections, 'name', 'misc');
        section.fields.push({
            $type: 'checkbox', 
            name: 'mailenabled', 
            flags: ['w_if_no_aci'],
            options: [
                { label: 'Mail enabled' }
            ],
            tooltip: {
                title: 'TRUE to enable, FALSE to disable account',
                html: true
            },
        });
        return true;	
    };

    phases.on('customization', mail_enabled_plugin.add_mail_enabled_pre_op);

    return mail_enabled_plugin;
});
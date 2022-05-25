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

    var mail_alias_plugin = {};

    // adds 'mailalias' field into user details facet
    mail_alias_plugin.add_mail_alias_pre_op = function() {
        var facet = get_item(IPA.user.entity_spec.facets, '$type', 'details');
        var section = get_item(facet.sections, 'name', 'misc');
        section.fields.push({
            $type: 'multivalued', 
            name: 'mailalias', 
            flags: ['w_if_no_aci'],
            options: [
                { label: 'Mail alias' }
            ],
            tooltip: {
                title: 'RFC822 Mailbox - mail alias',
                html: true
            },
        });
        return true;	
    };

    phases.on('customization', mail_alias_plugin.add_mail_alias_pre_op);

    return mail_alias_plugin;
});
define([
    'freeipa/phases',
    'freeipa/ipa'],
    function(phases, IPA) {
    
    // helper function
    function get_item(array, attr, value) {
        for (var i=0,l=array.length; i<l; i++) {
            if (array[i][attr] === value) return array[i];
        }
        return null;
    }

    var mail_sieve_rule_source_plugin = {};

    // adds 'mailsieverulesource' field into user details facet
    mail_sieve_rule_source_plugin.add_mail_sieve_rule_source_pre_op = function() {
        var facet = get_item(IPA.user.entity_spec.facets, '$type', 'details');
        var section = get_item(facet.sections, 'name', 'misc');
        section.fields.push({
            $type: 'multivalued', 
            name: 'mailsieverulesource', 
            flags: ['w_if_no_aci'],
            options: [
                { label: 'Mail Sieve rule source' }
            ],
            tooltip: {
                title: 'Sun ONE Messaging Server defined attribute',
                html: true
            },
        });
        return true;	
    };

    phases.on('customization', mail_sieve_rule_source_plugin.add_mail_sieve_rule_source_pre_op);

    return mail_sieve_rule_source_plugin;
});
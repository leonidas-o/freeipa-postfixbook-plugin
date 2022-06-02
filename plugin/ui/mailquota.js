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

    var mail_quota_plugin = {};

    // adds 'mailquota' field into user details facet
    mail_quota_plugin.add_mail_quota_pre_op = function() {
        var facet = get_item(IPA.user.entity_spec.facets, '$type', 'details');
        var section = get_item(facet.sections, 'name', 'misc');
        section.fields.push({
            $type: 'multivalued',
            name: 'mailquota',
            flags: ['w_if_no_aci'],
            options: [
                { label: 'Mail quota' }
            ],
            tooltip: {
                title: '<p>Mail quota limit in kilobytes</p><p>Allowed values are "", "none", "default", specific values like e.g. "1024 KB" (default is "default")</p>',
                html: true
            },
        });
        return true;	
    };

    phases.on('customization', mail_quota_plugin.add_mail_quota_pre_op);

    return mail_quota_plugin;
});






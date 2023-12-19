{{ partial("layout_partials/base_form",['fields':generalForm,'id':'frm_GeneralSettings'])}}
<script type="text/javascript">
    {% set usage_txt = 'In order to use this plugin, "Execute" Action should be set for Service Test and "/usr/local/opnsense/scripts/OPNsense/Monit2T/monit2t.sh" as a path.' %}
    $( document ).ready(function() {
        let help_row = '<tr><td><i class="fa fa-info-circle text-muted"></i> {{ lang._('Usage') }}</td><td>{{ lang._(usage_txt) }}&nbsp;<a href="#" class="text-danger" id="copy-path" title="Copy path to clipboard"><i class="fa fa-copy"></i></a></td><td></td></tr>'
        var data_get_map = {'frm_GeneralSettings':"/api/monit2t/settings/get"};
        mapDataToFormUI(data_get_map).done(function(data){
            $("#frm_GeneralSettings tbody").append(help_row);
            $("#copy-path").click(function () {
                $(this).fadeOut();
                navigator.clipboard.writeText('/usr/local/opnsense/scripts/OPNsense/Monit2T/monit2t.sh');
                $(this).fadeIn();
            });
        });

        $("#reconfigureAct").SimpleActionButton({
            onPreAction: function () {
                const dfObj = new $.Deferred();
                saveFormToEndpoint("/api/monit2t/settings/set", 'frm_GeneralSettings', function () { dfObj.resolve(); }, true, function () { dfObj.reject(); });
                return dfObj;
            }
        });

        $("#testAct").click(function(){
            $("#testAct_progress").addClass("fa fa-spinner fa-pulse");
            ajaxCall(url="/api/monit2t/service/test", sendData={}, callback=function(data,status) {
                $("#testAct_progress").removeClass("fa fa-spinner fa-pulse");
                if (data['status'].indexOf('error') > -1) {
                    BootstrapDialog.show({
                        type: BootstrapDialog.TYPE_DANGER,
                        title: "{{ lang._('Error sending test message') }}",
                        message: "Telegram API returned: " + data['msg'],
                        draggable: true
                    });
                } else {
                    BootstrapDialog.show({
                        type: BootstrapDialog.TYPE_WARNING,
                        title: "{{ lang._('Test message sent successfully') }}",
                        message: "{{ lang._('Test message sent successfully.') }}",
                        draggable: true
                    });
                }
            });
        });
    });
</script>

<div class="col-md-12 __mt">
        <button class="btn btn-primary" id="reconfigureAct"
            data-endpoint="/api/monit2t/service/reconfigure"
            data-label="Apply"
            data-error-title="Error reconfiguring Monit2T"
            type="button">
        </button>
        <button class="btn btn-primary" id="testAct" type="button"><b>{{ lang._('Send test message') }}</b><i id="testAct_progress"></i></button>
</div>


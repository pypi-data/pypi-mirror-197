// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable();
});

// Call multiple select plugin
$('#selectAllDomainList').click(function() {
  var checkedStatus = this.checked;
  $('#dataTable tbody tr').find('td:first :checkbox').each(function() {
    $(this).prop('checked', checkedStatus);
  });
});

// Toggle select
$('#bulkEditHeaderCancel').click(function(){
    $('#bulkEditHeader').addClass('d-none');
    $('.form-selector.selector').addClass('d-none');
});
$('#bulkEditBtn').click(function(){
    $('#bulkEditHeader').removeClass('d-none');
    $('.form-selector.selector.d-none').removeClass('d-none');
});
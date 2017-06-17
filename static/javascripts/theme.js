// Theme custom js methods
$(document).ready(function(){

  // Custom warnings and notes
  var addChartsAlert = function(selector) {
    var str = {
      'es': 'Los datos de 2017 están actualizados a 12 de junio.',
      'gl': 'Os datos de 2017 están actualizados ao 12 de xuño.'
    };
    var cont = $(selector);
    if (cont.size() > 0) {
      cont.prepend('<div class="alert alert-data-update">' + str[$('html').attr('lang')] + '</div>');
    }
  };

  var addBudgetClarification = function() {
    var str = {
      'es': 'Las cantidades presupuestadas se refieren a créditos iniciales.',
      'gl': 'As cantidades orzadas refírense a créditos iniciais.'
    };
    var cont = $('.budget-totals').find('small');
    if (cont.size() > 0) {
      cont.append(str[$('html').attr('lang')]);
    }
    var cont = $('.data-controllers + #totals-panel');
    if (cont.size() > 0) {
      cont.append('<p class="text-center" style="margin-top: 1em"><small>' + str[$('html').attr('lang')] + '</small></p>');
    }
  };

  addChartsAlert('.policies-chart');
  addChartsAlert('.sankey-container');

  addBudgetClarification();

});

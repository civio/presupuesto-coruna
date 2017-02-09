// Theme custom js methods
$(document).ready(function(){

  // Custom warnings and notes
  var addChartsAlert = function(selector) {
    var str = {
      'es': 'Los datos de ejecución del año 2016 son provisionales y están pendientes del cierre de ejercicio',
      'gl': 'Os datos de execución do ano 2016 son provisionais e están pendentes do peche de exercicio'
    };
    var cont = $(selector);
    if (cont.size() > 0) {
      cont.prepend('<div class="alert alert-data-update">' + str[$('html').attr('lang')] + '</div>');
    }
  };

  var addBudgetClarification = function() {
    var str = {
      'es': 'Las cantidades presupuestadas se refieren a créditos iniciales.',
      'gl': 'As cantidades orzadas se refiren a créditos iniciais.'
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

// Custom data table formatters
function getFormatter(formatter, stats, year, getter) {
  // theme.js version
  // Pretty print a number by inserting ',' thousand separator
  function nominalFormatter(value, type, item) {
    if (type === 'filter') return value;  // We filter based on the raw data
    return formatAmount(value);
  }

  // Display amount adjusted for inflation (real, versus nominal)
  function realFormatter(value, type, item) {
    if (value == null) return '';
    if (type === 'filter') return value;  // We filter based on the raw data
    var realValue = adjustInflation(value, stats, year);
    return formatAmount(realValue);
  }

  // Display amount as percentage of total
  function percentageFormatter(value, type, item) {
    if (value == null) return '';
    if (type === 'filter') return value;  // We filter based on the raw data
    if (item.root == null)  // No root => independent object
      return formatPercentage(1);
    else
      return formatPercentage(value / columnValueExtractor(item.root, getter));
  }

  // Display amount as expense per capita
  function perCapitaFormatter(value, type, item) {
    if (value == null) return '';
    if (type === 'filter') return value;  // We filter based on the raw data
    // Note value is in cents originally
    var realValue = adjustInflation(value/100, stats, year);

    // Our stats for year X indicate the population for December 31st of that year so,
    // since we're adjusting inflation for January 1st it seems more accurate to use the
    // population for that date, i.e. the one for the last day of the previous year.
    // XXX: Don't think this is still so, and it's confusing, so I've changed it. But
    // would like to recheck it.
    var population = getPopulationFigure(stats, year, item.key);

    return addCurrencySymbol(formatDecimal(realValue / population));
  }

  // Display execution amount as percentage of total
  function executionPercentageFormatter(value, type, item) {
    if (value == null) return '';
    if (type === 'filter') return value;  // We filter based on the raw data
    if (item.root == null)  return formatPercentage(1); // No root => independent object
    
    return formatPercentage(value / columnValueExtractor(item.root, getter));
  }

  switch (formatter) {
    case "nominal":              return nominalFormatter;
    case "real":                 return realFormatter;
    case "percentage":           return percentageFormatter;
    case "per_capita":           return perCapitaFormatter;
    case "execution_percentage": return executionPercentageFormatter;
  }
}
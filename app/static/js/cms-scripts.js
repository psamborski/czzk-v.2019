$(document).ready(function(){
    $('.sidenav').sidenav();

    $('.collapsible').collapsible();

    $('.datepicker').datepicker({
        firstDay: true,
        format: 'dd.mm.yyyy',
        i18n: {
            cancel: 'Anuluj',
            months: ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"],
            monthsShort: ["Sty", "Lut", "Mar", "Kwi", "Maj", "Cze", "Lip", "Sie", "Wrz", "Paź", "Lis", "Gru"],
            weekdays: ["Niedziela","Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
            weekdaysShort: ["Nie","Pon", "Wt", "Śr", "Czw", "Pt", "Sob"],
            weekdaysAbbrev: ["N","P", "W", "Ś", "C", "P", "S"]
        },
    });
    $('.timepicker').timepicker({
        twelveHour: false,
        showClearBtn: true,
        i18n: {
            cancel: 'Anuluj',
            done: 'OK',
            clear: 'Wyczyść'
        },
    });

    $('textarea').characterCounter();

    $('.modal').modal();
    $('select').formSelect();
});
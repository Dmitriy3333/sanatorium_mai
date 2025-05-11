// вывод выбора страны, региона и курорта - с зависимостями  
const geoData = [
    {
        country: "Россия",
        regions: [
            { region: "Московская область", resorts: ["Звенигород", "Сергиев Посад", "Коломна", "Дмитров", "Истра", "Клин", "Серпухов", "Жуковский"] },
            { region: "Ленинградская область", resorts: ["Выборг", "Гатчина", "Пушкин", "Петергоф", "Кронштадт", "Приозерск", "Сосновый Бор", "Тихвин"] },
            { region: "Краснодарский край", resorts: ["Сочи", "Анапа", "Геленджик", "Туапсе", "Адлер", "Новороссийск", "Архипо-Осиповка", "Лазаревское"] },
            { region: "Ставропольский край", resorts: ["Кисловодск", "Ессентуки", "Пятигорск", "Железноводск", "Минеральные Воды", "Невинномысск", "Будённовск"] },
            { region: "Алтайский край", resorts: ["Белокуриха", "Горный Алтай", "Чемал", "Телецкое озеро", "Артыбаш", "Ая", "Манжерок", "Турочак"] },
            { region: "Крым", resorts: ["Ялта", "Евпатория", "Севастополь", "Феодосия", "Алушта", "Судак", "Керчь", "Бахчисарай"] },
            { region: "Карелия", resorts: ["Петрозаводск", "Сортавала", "Рускеала", "Валаам", "Кижи", "Кондопога", "Медвежьегорск", "Беломорск"] },
            { region: "Калининградская область", resorts: ["Калининград", "Светлогорск", "Зеленоградск", "Янтарный", "Куршская коса", "Балтийск", "Советск", "Черняховск"] },
            { region: "Золотое кольцо России", resorts: ["Владимир", "Суздаль", "Ярославль", "Кострома", "Иваново", "Ростов Великий", "Переславль-Залесский", "Углич"] },
            { region: "Кавказские Минеральные Воды", resorts: ["Железноводск", "Кисловодск", "Ессентуки", "Пятигорск", "Минеральные Воды", "Лермонтов", "Иноземцево"] },
            { region: "Байкал", resorts: ["Иркутск", "Листвянка", "Аршан", "Байкальск", "Слюдянка", "Ольхон", "Улан-Удэ", "Горячинск"] },
            { region: "Дальний Восток", resorts: ["Владивосток", "Хабаровск", "Находка", "Артём", "Уссурийск", "Петропавловск-Камчатский", "Южно-Сахалинск", "Благовещенск"] },
            { region: "Урал", resorts: ["Екатеринбург", "Челябинск", "Пермь", "Уфа", "Тюмень", "Магнитогорск", "Нижний Тагил", "Златоуст"] },
            { region: "Сибирь", resorts: ["Новосибирск", "Омск", "Красноярск", "Барнаул", "Томск", "Кемерово", "Новокузнецк", "Абакан"] },
            { region: "Другой", resorts: ["Другой"] }
        ]
    },
    {
        country: "Казахстан",
        regions: [
            { region: "Алматы", resorts: ["Медео", "Шымбулак", "Большое Алматинское озеро", "Тургень", "Чимбулак"] },
            { region: "Астана", resorts: ["Бурабай", "Щучинск", "Коргалжын", "Боровое", "Зеренда"] },
            { region: "Павлодар", resorts: ["Баянаул", "Аксу", "Экибастуз", "Железинка", "Павлодар"] },
            { region: "Актау", resorts: ["Жанаозен", "Форт-Шевченко", "Баутино", "Кендерли", "Шетпе"] },
            { region: "Другой", resorts: ["Другой"] }
        ]
    },
    {
        country: "Беларусь",
        regions: [
            { region: "Минская область", resorts: ["Несвиж", "Борисов", "Мир", "Заславль", "Логойск"] },
            { region: "Гродненская область", resorts: ["Гродно", "Лида", "Новогрудок", "Слоним", "Берёзовка"] },
            { region: "Брестская область", resorts: ["Брест", "Кобрин", "Пинск", "Беловежская пуща", "Каменец"] },
            { region: "Витебская область", resorts: ["Витебск", "Полоцк", "Орша", "Браслав", "Глубокое"] },
            { region: "Другой", resorts: ["Другой"] }
        ]
    },
    {
        country: "Узбекистан",
        regions: [
            { region: "Ташкент", resorts: ["Чарвак", "Янгибазар", "Бричмулла", "Хумсан", "Газалкент"] },
            { region: "Самарканд", resorts: ["Ургут", "Паянда", "Зарафшан", "Джамбай", "Акташ"] },
            { region: "Бухара", resorts: ["Газли", "Каган", "Ромитан", "Шафиркан", "Вабкент"] },
            { region: "Фергана", resorts: ["Коканд", "Маргилан", "Кува", "Риштан", "Кувасай"] },
            { region: "Другой", resorts: ["Другой"] }
        ]
    },
    {
        country: "Другое",
        regions: [
            { region: "Другой", resorts: ["Другой"] }
        ]
    }
];

const countrySelect = document.getElementById("country");
const regionSelect = document.getElementById("region");
const resortSelect = document.getElementById("resort");

const selectedCountry = countrySelect.dataset.selected;
const selectedRegion = regionSelect.dataset.selected;
const selectedResort = resortSelect.dataset.selected;

// Далее логика инициализации:
populateSelect(countrySelect, geoData.map(c => c.country), selectedCountry);
updateRegions(); // внутри неё уже используется selectedRegion и т.д.


function populateSelect(select, options, selectedValue) {
    select.innerHTML = "";
    for (var i = 0; i < options.length; i++) {
        var option = document.createElement("option");
        option.value = options[i];
        option.text = options[i];
        if (options[i] === selectedValue) {
            option.selected = true;
        }
        select.appendChild(option);
    }
}

function updateRegions() {
    var selectedCountryName = countrySelect.value;
    var regions = [];
    for (var i = 0; i < geoData.length; i++) {
        if (geoData[i].country === selectedCountryName) {
            var regionList = geoData[i].regions;
            for (var j = 0; j < regionList.length; j++) {
                regions.push(regionList[j].region);
            }
            break;
        }
    }
    populateSelect(regionSelect, regions, selectedRegion);
    updateResorts();
}

function updateResorts() {
    var selectedCountryName = countrySelect.value;
    var selectedRegionName = regionSelect.value;
    var resorts = [];
    for (var i = 0; i < geoData.length; i++) {
        if (geoData[i].country === selectedCountryName) {
            var regionList = geoData[i].regions;
            for (var j = 0; j < regionList.length; j++) {
                if (regionList[j].region === selectedRegionName) {
                    resorts = regionList[j].resorts;
                    break;
                }
            }
            break;
        }
    }
    populateSelect(resortSelect, resorts, selectedResort);
}

window.addEventListener("DOMContentLoaded", function() {
    var countries = [];
    for (var i = 0; i < geoData.length; i++) {
        countries.push(geoData[i].country);
    }
    populateSelect(countrySelect, countries, selectedCountry);
    updateRegions();
});

countrySelect.addEventListener("change", updateRegions);
regionSelect.addEventListener("change", updateResorts);


// управление слайдером
document.querySelectorAll('.photo').forEach(carousel => {
    const imgWrap = carousel.querySelector('.img-wrap');
    const imgs = carousel.querySelectorAll('.img-wrap img');
    const prevBtn = carousel.querySelector('.prev');
    const nextBtn = carousel.querySelector('.next');
    let idx = 0;

    function showImg() {
        if (idx >= imgs.length) idx = 0;
        if (idx < 0) idx = imgs.length - 1;
        imgWrap.style.transform = `translateX(-${idx * 100}%)`;
    }

    nextBtn.addEventListener('click', (e) => {
        e.stopPropagation();  
        idx++;
        showImg();
    });

    prevBtn.addEventListener('click', (e) => {
        e.stopPropagation();  // Prevents triggering the sanatorium link
        idx--;
        showImg();
    });

    showImg();
});
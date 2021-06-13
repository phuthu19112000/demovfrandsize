// https://www.belstaff.co.uk/customer-service/womens-sizing-chart.html

let uksizes = new Map();
uksizes.set(4,"XXS");
uksizes.set(6,"XS")
uksizes.set(8,"S");
uksizes.set(10,"M");
uksizes.set(12,"L");
uksizes.set(14,"XL");
uksizes.set(16,"XXL");
uksizes.set(18,"XXL");

const skirtSizeChart=[
    {"size":4, "natural_waist": 60.5, "low_waist": 77, "hip": 85.5},
    {"size":6, "natural_waist": 64.5, "low_waist": 81, "hip": 89.5},
    {"size":8, "natural_waist": 68.5, "low_waist": 85, "hip": 93.5},
    {"size":10, "natural_waist": 72.5, "low_waist": 89,"hip": 97.5},
    {"size":12, "natural_waist": 76.5, "low_waist": 93,"hip": 101.5},
    {"size":14, "natural_waist": 80.5, "low_waist": 97,"hip": 105.5},
    {"size":16, "natural_waist": 84.5, "low_waist": 101,"hip": 109.5}
]

const dressSizeChart = [
    {"size":4, "bust": 78, "waist": 60, "hip": 83.5},
    {"size":6, "bust": 80.5, "waist": 62.5, "hip": 86},
    {"size":8, "bust": 83, "waist": 65, "hip": 88.5},
    {"size":10, "bust": 88, "waist": 70, "hip": 93.5},
    {"size":12, "bust": 93, "waist": 75, "hip": 98.5},
    {"size":14, "bust": 98, "waist": 80, "hip": 103.5},
    {"size":16, "bust": 103, "waist": 85, "hip": 108.5},
    {"size":18, "bust": 110.5, "waist": 92.5, "hip": 116.5}
]

const jacketsSizeChart = [
    {"size":"S", "bust": cm(36.2), "hip": cm(37.8), "sleeve": cm(27.1)},
    {"size":"M", "bust": cm(38.4), "hip": cm(40), "sleeve": cm(27.5)},
    {"size":"L", "bust": cm(40.8), "hip": cm(42.4), "sleeve": cm(27.9)},
    {"size":"XL", "bust": cm(43.2), "hip": cm(44.8), "sleeve": cm(28.3)},
    {"size":"XXL", "bust": cm(45.6), "hip": cm(47.2), "sleeve": cm(28.7)}
]

const jeansSizeChart=[
    {"size":6, "waist": cm(24), "hip": cm(16.7), "thigh": cm(9.2), "frontrise": cm(7.1), "backrise": cm(12.2), "knee": cm(5.9), "legopening": cm(5.1)},
    {"size":8, "waist": cm(26), "hip": cm(17.7), "thigh": cm(9.8), "frontrise": cm(7.5), "backrise": cm(12.6), "knee": cm(6.3), "legopening": cm(5.5)},
    {"size":10, "waist": cm(28), "hip": cm(18.7), "thigh": cm(10.4), "frontrise": cm(7.9), "backrise": cm(13), "knee": cm(6.7), "legopening": cm(5.9)},
    {"size":12, "waist": cm(30), "hip": cm(19.7), "thigh": cm(11), "frontrise": cm(8.3), "backrise": cm(13.4), "knee": cm(7.1), "legopening": cm(6.3)},
    {"size":14, "waist": cm(32), "hip": cm(20.7), "thigh": cm(11.6), "frontrise": cm(8.7), "backrise": cm(13.8), "knee": cm(7.5), "legopening": cm(6.7)},
    {"size":16, "waist": cm(34), "hip": cm(21.7), "thigh": cm(12.2), "frontrise": cm(9.1), "backrise": cm(14.2), "knee": cm(7.9), "legopening": cm(7.1)},
    {"size":18, "waist": cm(36), "hip": cm(22.7), "thigh": cm(12.8), "frontrise": cm(9.5), "backrise": cm(14.6), "knee": cm(8.3), "legopening": cm(7.5)},
    {"size":20, "waist": cm(40), "hip": cm(23.7), "thigh": cm(13.4), "frontrise": cm(9.9), "backrise": cm(15), "knee": cm(8.7), "legopening": cm(7.9)}
]

const tshirtSizeChart=[
    {"size":"XS", "bust": cm(32), "len": cm(23), "shoulder": cm(14), "sleevelen": cm(5.5), "sleeveopen": cm(5)},
    {"size":"S", "bust": cm(34), "len": cm(24), "shoulder": cm(15), "sleevelen": cm(6), "sleeveopen": cm(5.5)},
    {"size":"M", "bust": cm(36), "len": cm(25), "shoulder": cm(16), "sleevelen": cm(6.5), "sleeveopen": cm(5.5)},
    {"size":"L", "bust": cm(38), "len": cm(26), "shoulder": cm(17), "sleevelen": cm(7), "sleeveopen": cm(6)},
    {"size":"XL", "bust": cm(40), "len": cm(27), "shoulder": cm(18), "sleevelen": cm(7.5), "sleeveopen": cm(6.5)},
    {"size":"XXL", "bust": cm(41), "len": cm(28), "shoulder": cm(19), "sleevelen": cm(8), "sleeveopen": cm(7)}
]

function cm(inches){
    return (2.54*inches);
}

const getSkirtSize = function(skirtSizeChart,form){
    let input = fillInputArray(form);
    let mindiffsum = 1000;
    let minsize = skirtSizeChart[0].size;

    for(let size of skirtSizeChart){
        let diff1=0, diff2=0, diff3=0;
        if(input.natural_waist)diff1= Math.abs(size.natural_waist - input.natural_waist);
        if(input.low_waist)diff2= Math.abs(size.low_waist - input.low_waist)
        if(input.hip)diff3 = Math.abs(size.hip - input.hip);

        let sumdiff = diff1 + diff2 + diff3;
        if(sumdiff <= mindiffsum){
            mindiffsum = sumdiff;
            minsize = size.size;
        }
    }
    return uksizes.get(minsize);
}

const getDressSize = function(dressSizeChart,form){
    let input = fillInputArray(form);
    let mindiffsum = 1000;
    let minsize = dressSizeChart[0].size;

    for(let size of dressSizeChart){
        let diff1 = 0, diff2 = 0, diff3 = 0;
        if(input.bust)diff1 = Math.abs(size.bust - input.bust);
        if(input.waist)diff2 = Math.abs(size.waist - input.waist);
        if(input.hip)diff3 = Math.abs(size.hip - input.hip);

        let sumdiff = diff1 + diff2 + diff3;
        if(sumdiff <= mindiffsum){
            mindiffsum = sumdiff;
            minsize = size.size;
        }
    }
    return uksizes.get(minsize);
}

const getJacketSize = function(jacketsSizeChart,form){
    let input = fillInputArray(form);
    let mindiffsum = 1000;
    let minsize = jacketsSizeChart[0].size;

    for(let size of jacketsSizeChart){
        let diff1 = 0, diff2 = 0, diff3 = 0;
        if(input.bust)diff1 = Math.abs(size.bust - input.bust);
        if(input.hip)diff2 = Math.abs(size.hip - input.hip);
        if(input.sleeve)diff3 = Math.abs(size.sleeve - input.sleeve);

        let sumdiff = diff1 + diff2 + diff3;
        if(sumdiff <= mindiffsum){
            mindiffsum = sumdiff;
            minsize = size.size;
        }
    }
    return minsize;
}


const getJeanSize = function(jeansSizeChart,form){
    let input = fillInputArray(form);
    let mindiffsum = 1000;
    let minsize = jeansSizeChart[0].size;

    for(let size of jeansSizeChart){
        let diff1 = 0, diff2 = 0, diff3 = 0;
        if(input.waist)diff1 = Math.abs(size.waist - input.waist);
        if(input.hip)diff2 = Math.abs(size.hip - input.hip);
        if(input.thigh)diff3 = Math.abs(size.thigh - input.thigh);

        let sumdiff = diff1 + diff2 + diff3;
        if(sumdiff <= mindiffsum){
            mindiffsum = sumdiff;
            minsize = size.size;
        }
    }
    return uksizes.get(minsize);
}

const getTshirtSize= function(tshirtSizeChart,form){
    let input= fillInputArray(form);
    let mindiffsum= 1000;
    let minsize= tshirtSizeChart[0].size;

    for(let size of tshirtSizeChart){
        let diff1=0, diff2= 0, diff3=0, diff4= 0;

        if(input.bust)diff1= Math.abs(size.bust-input.bust);
        if(input.len)diff2= Math.abs(size.len-input.len);
        if(input.shoulder)diff3= Math.abs(size.shoulder-input.shoulder);
        if(input.sleevelen)diff4= Math.abs(size.sleevelen-input.sleevelen);

        let sumdiff= diff1+diff2+diff3+diff4
        if(sumdiff<= mindiffsum){
            mindiffsum= sumdiff;
            minsize= size.size;
        }
    }
    return minsize; 
}

const getLeggingSize = function(jeansSizeChart,form){
    let input = fillInputArray(form);
    let mindiffsum = 1000;
    let minsize = jeansSizeChart[0].size;

    for(let size of jeansSizeChart){
        let diff1=0, diff2 = 0, diff3 = 0
        
        if(input.waist)diff1 = Math.abs(size.waist - input.waist);
        if(input.hip)diff2 = Math.abs(size.hip - input.hip);
        
        let sumdiff = diff1 + diff2;
        if(sumdiff <= mindiffsum){
            mindiffsum = sumdiff;
            minsize = size.size;
        }
    }
    return minsize
}

function fillInputArray(form){

    let input= [
        {"bust":0},
        {"hip":0},
        {"len":0},
        {"hem":0},
        {"natural_waist":0},
        {"low_waist":0},
        {"shoulder":0},
        {"sleevelen":0},
        {"sleeveopen":0},
        {"necktoshoulder":0},
        {"frontrise":0},
        {"thigh":0},
        {"knee":0},
        {"legopening":0},
        {"inseam":0}
    ];

    if(form.elements.bust) input.bust= form.elements.bust.value;
    if(form.elements.natural_waist) input.natural_waist= form.elements.natural_waist.value;
    if(form.elements.hip) input.hip= form.elements.hip.value;
    if(form.elements.len) input.len= form.elements.len.value;
    if(form.elements.hem) input.hem= form.elements.hem.valsleevelen
    if(form.elements.low_waist) input.low_waist= form.elements.low_waist.value;
    if(form.elements.shoulder) input.shoulder= form.elements.shoulder.valshoulder
    if(form.elements.sleevelen) input.sleevelen= form.elements.sleevelen.value;
    if(form.elements.sleeveopen) input.sleeveopen= form.elements.sleeveopen.value;
    if(form.elements.necktoshoulder) input.necktoshoulder= form.elements.necktoshoulder.value;
    if(form.elements.frontrise) input.frontrise= form.elements.frontrise.value;
    if(form.elements.thigh) input.thigh= form.elements.thilegopening
    if(form.elements.legopening) input.legopening= form.elements.legopening.value;
    if(form.elements.inseam) input.inseam= form.elements.inseam.value;
    
    return input;
}

let products=[
    {"num":1, "sizechart": skirtSizeChart, "fn": getSkirtSize},
    {"num":2, "sizechart": tshirtSizeChart, "fn": getTshirtSize},
    {"num":3, "sizechart": skirtSizeChart, "fn": getSkirtSize},
    {"num":4, "sizechart": tshirtSizeChart, "fn": getTshirtSize},
    {"num":5, "sizechart": jeansSizeChart, "fn": getJeanSize},
    {"num":6, "sizechart": dressSizeChart, "fn": getDressSize},
    {"num":7, "sizechart": dressSizeChart, "fn": getDressSize}
]

for(let product of products){
    let form= document.querySelector(`#form${product.num}`);
    form.addEventListener("submit", function(event){    
        event.preventDefault(); //will prevent refreshing of the page on clicking the button
        document.getElementById(`result${product.num}`).textContent = "";
        console.log("event fired");
        let result= product.fn(product.sizechart,form); 
        if(result)document.getElementById(`result${product.num}`).textContent += `Your best fit would be size: ${result}`;
        else document.getElementById(`result${product.num}`).textContent += `Sorry we don't have a similar sized product`;
    });

    //close buttons
    let close= document.querySelector(`#close${product.num}`);
    close.addEventListener("click", function(){
        clearFields(form,product.num);
    });
}

function clearFields(form,num){
    for(let i=0; i<form.elements.length-2; i++){
        form.elements[i].value= "";
    }
    document.getElementById(`result${num}`).textContent = "";
}
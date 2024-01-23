let names;
async function getNames() {
    let url = 'api/company_names'
    response = await fetch(url);
    names = await response.json();
}
getNames();
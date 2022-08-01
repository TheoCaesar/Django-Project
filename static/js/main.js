//get searchform from finalproj.html and page links from lines 7 to 23
//step 2
let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link') 
//check if searchForm exists
if(searchForm){
for(let i = 0; pageLinks.length> i; i++)
    {
      pageLinks[i].addEventListener('click', function(e) {      //second arg is somewhat of an inline fxn
        e.preventDefault()
        //console.log('Button click') //tested and it worked -- step 2

        //step 4 -- GET DATA-PAGE ATTRIBUTE
        let page = this.dataset.page    //'this' is js equivalent of self in python
        //console.log('You clicked page ' , page)

        //STEP 5 -- Add hidden search input to form
        searchForm.innerHTML += `<input value = ${page} name  = "page" hidden/>`
        //not that these aren't quotation marks but back ticks, the symbol on key above the tab key.
        //may be referred to as template literals

        //SUBMIT FORM
        searchForm.submit()
      })
    }
  }
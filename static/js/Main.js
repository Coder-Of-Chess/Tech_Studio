

    // on page load collect data to load pagination as well as table

    // At a time maximum allowed pages to be shown in pagination div
    const pagination_visible_pages = 100;


    // hide pages from pagination from beginning if more than pagination_visible_pages
function hide_from_beginning(element) {
    if (element.style.display === "" || element.style.display === "block") {
        element.style.display = "none";
    } else {
        hide_from_beginning(element.nextSibling);
    }
}

// hide pages from pagination ending if more than pagination_visible_pages
function hide_from_end(element) {
    if (element.style.display === "" || element.style.display === "block") {
        element.style.display = "none";
    } else {
        hide_from_beginning(element.previousSibling);
    }
}

// load data and style for active page
function active_page(element, rows, req_per_page) {
    var current_page = document.getElementsByClassName('active');
    var next_link = document.getElementById('next_link');
    var prev_link = document.getElementById('prev_link');
    var next_tab = current_page[0].nextSibling;
    var prev_tab = current_page[0].previousSibling;
    current_page[0].className = current_page[0].className.replace("active", "");
    if (element === "next") {
        if (parseInt(next_tab.text).toString() === 'NaN') {
            next_tab.previousSibling.className += " active";
            next_tab.setAttribute("onclick", "return false");
        } else {
            next_tab.className += " active"
            render_table_rows(rows, parseInt(req_per_page), parseInt(next_tab.text));
            render_products(rows, parseInt(req_per_page), parseInt(element.text));
            if (prev_link.getAttribute("onclick") === "return false") {
                prev_link.setAttribute("onclick", `active_page('prev',\"${rows}\",${req_per_page})`);
            }
            if (next_tab.style.display === "none") {
                next_tab.style.display = "block";
                hide_from_beginning(prev_link.nextSibling)
            }
        }
    } else if (element === "prev") {
        if (parseInt(prev_tab.text).toString() === 'NaN') {
            prev_tab.nextSibling.className += " active";
            prev_tab.setAttribute("onclick", "return false");
        } else {
            prev_tab.className += " active";
            render_products(rows, parseInt(req_per_page), parseInt(element.text));
            if (next_link.getAttribute("onclick") === "return false") {
                next_link.setAttribute("onclick", `active_page('next',\"${rows}\",${req_per_page})`);
            }
            if (prev_tab.style.display === "none") {
                prev_tab.style.display = "block";
                hide_from_end(next_link.previousSibling)
            }
        }
    } else {
        element.className += "active";
        render_products(rows, parseInt(req_per_page), parseInt(element.text));
        if (prev_link.getAttribute("onclick") === "return false") {
            prev_link.setAttribute("onclick", `active_page('prev',\"${rows}\",${req_per_page})`);
        }
        if (next_link.getAttribute("onclick") === "return false") {
            next_link.setAttribute("onclick", `active_page('next',\"${rows}\",${req_per_page})`);
        }
    }
}

// Render the table's row in table request-table
function render_table_rows(rows, req_per_page, page_no) {
    const response = JSON.parse(window.atob(rows));
    const resp = response.slice(req_per_page * (page_no - 1), req_per_page * page_no)
    $('#request-table').empty()
    $('#request-table').append('<tr><th>Index</th><th>Request No</th><th>Title</th></tr>');
    resp.forEach(function (element, index) {
        if (Object.keys(element).length > 0) {
            const { req_no, title } = element;
            const td = `<tr><td>${++index}</td><td>${req_no}</td><td>${title}</td></tr>`;
            $('#request-table').append(td)
        }
    });
}
function render_products(rows, req_per_page, page_no) {
    const response = JSON.parse(window.atob(rows));
    console.log(req_per_page,page_no,'hlll')
    const resp = response.slice(req_per_page * (page_no - 1), req_per_page * page_no)
    $('#product_here').empty()
    resp.forEach(function (element, index) {
        if (Object.keys(element).length > 0) {
            const { image, name, price, id } = element;
            const td = `
                <div class="col-lg-4 col-md-6 col-12">
                    <a href="https://greatknightschess.com/productDetails/${id}/">
                        <div class="card product-card" style="height: auto;">
                            <div class="product-img">
                                <img src="${image}" class=""
                                    alt="...">
                            </div>
                            <div class="card-body product-card-body">
                                <h5 class="card-title"><strong>${name}</strong></h5>
                                <p class="card-text">${price}</p>

                            </div>
                        </div>
                    </a>
                </div>
            `;
            $('#product_here').append(td)
        }
    });
}

// Pagination logic implementation
function pagination(data, myarr) {
    const all_data = window.btoa(JSON.stringify(myarr));
    $(".pagination").empty();
    console.log(data.req_per_page,'another one')
    if (data.req_per_page !== 'ALL') {
        let pager = `<a href="#" id="prev_link" onclick=active_page('prev',\"${all_data}\",${data.req_per_page})>&laquo;</a>` +
            `<a href="#" class="active" onclick=active_page(this,\"${all_data}\",${data.req_per_page})>1</a>`;
        const total_page = Math.ceil(parseInt(myarr.length) / parseInt(data.req_per_page));
        if (total_page < pagination_visible_pages) {
            render_products(all_data, data.req_per_page, data.page_no);
            for (let num = 2; num <= total_page; num++) {
                pager += `<a href="#" onclick=active_page(this,\"${all_data}\",${data.req_per_page})>${num}</a>`;
            }
        } else {
            render_products(all_data, data.req_per_page, data.page_no);
            for (let num = 2; num <= pagination_visible_pages; num++) {
                pager += `<a href="#" onclick=active_page(this,\"${all_data}\",${data.req_per_page})>${num}</a>`;
            }
            for (let num = pagination_visible_pages + 1; num <= total_page; num++) {
                pager += `<a href="#" style="display:none;" onclick=active_page(this,\"${all_data}\",${data.req_per_page})>${num}</a>`;
            }
        }
        pager += `<a href="#" id="next_link" onclick=active_page('next',\"${all_data}\",${data.req_per_page})>&raquo;</a>`;
        $(".pagination").append(pager);
    } else {
        render_products(all_data, myarr.length, 1);
        console.log('hello')
    }
}

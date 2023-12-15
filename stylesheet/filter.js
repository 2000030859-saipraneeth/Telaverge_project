// Get unique values for the desired columns

// {2 : ["M", "F"], 3 : ["RnD", "Engineering", "Design"], 4 : [], 5 : []}

function getUniqueValuesFromColumn() {

    var unique_col_values_dict = {}

    allFilters = document.querySelectorAll(".table-filter")
    allFilters.forEach((filter_i) => {
        col_index = filter_i.parentElement.getAttribute("col-index");
        // alert(col_index)
        const rows = document.querySelectorAll("#emp-table > tbody > tr")

        rows.forEach((row) => {
            cell_value = row.querySelector("td:nth-child("+col_index+")").innerHTML;
            // if the col index is already present in the dict
            if (col_index in unique_col_values_dict) {

                // if the cell value is already present in the array
                if (unique_col_values_dict[col_index].includes(cell_value)) {
                    // alert(cell_value + " is already present in the array : " + unique_col_values_dict[col_index])

                } else {
                    unique_col_values_dict[col_index].push(cell_value)
                    // alert("Array after adding the cell value : " + unique_col_values_dict[col_index])

                }


            } else {
                unique_col_values_dict[col_index] = new Array(cell_value)
            }
        });


    });

//    for(i in unique_col_values_dict) {
//        alert("Column index : " + i + " has Unique values : \n" + unique_col_values_dict[i]);
//    }

    updateSelectOptions(unique_col_values_dict)

};

// Add <option> tags to the desired columns based on the unique values

function updateSelectOptions(unique_col_values_dict) {
    allFilters = document.querySelectorAll(".table-filter")

    allFilters.forEach((filter_i) => {
        col_index = filter_i.parentElement.getAttribute('col-index')

         filter_i.innerHTML = '<option value="all">All</option>';

        unique_col_values_dict[col_index].forEach((i) => {
            filter_i.innerHTML = filter_i.innerHTML + `\n<option value="${i}">${i}</option>`
        });

    });
};

const searchhash=()=>{

let filter=document.getElementById('hash').value.toUpperCase();
const hashtags = filter.replace(/#/g, ' ').split(' ');
const trimmedHashtags = hashtags.map(hashtag => hashtag.trim());
const filteredHashtags = trimmedHashtags.filter(hashtag => hashtag !== '');
console.log(filteredHashtags)
let myTable=document.getElementById('emp-table');

let tr=myTable.getElementsByTagName('tr')
for(var i=2;i<tr.length;i++){
let td=tr[i].innerText.toUpperCase();
var flag = filteredHashtags.every(tag => td.includes(tag));
//logic to find same
if(flag){
tr[i].style.display="";
}else{
tr[i].style.display="none";
}




}

}

// Create filter_rows() function
//sorting
let currentSortOrder = []; // Array to store the current sort order

function sortRows1() {
    console.log("sortRows function called");
    const selectedSorter = document.querySelector(".table-sorter1");

    if (!selectedSorter) {
        console.log("No sortRows function ");
        return; // No sorting option selected
    }

    const col_index = selectedSorter.parentElement.getAttribute("col-index");
    const order = selectedSorter.value;

    // Find the index of the column in the currentSortOrder array
    const existingSortIndex = currentSortOrder.findIndex((sort) => sort.colIndex === col_index);
    console.log(existingSortIndex)

    if (existingSortIndex !== -1) {
        // Column already exists in the sort order, update its order
//        currentSortOrder[existingSortIndex].order = order;
         currentSortOrder=[]
        currentSortOrder.push({ colIndex: col_index, order: order });
//        console.log(order)
        console.log(currentSortOrder)
        console.log("flag 0"+ order)
    } else {
        // Column does not exist in the sort order, add it
        currentSortOrder.push({ colIndex: col_index, order: order });
        console.log(currentSortOrder)
    }

    // Apply sorting based on the current sort order
    const rows = Array.from(document.querySelectorAll("#emp-table tbody tr"));

    const sortedRows = rows.sort((a, b) => {
        let result = 0;

        currentSortOrder.forEach((sort) => {
            const valueA = parseInt(a.querySelector(`td:nth-child(${sort.colIndex})`).textContent);
            const valueB = parseInt(b.querySelector(`td:nth-child(${sort.colIndex})`).textContent);

            if (sort.order === "asc") {
                result = valueA - valueB;
            } else {
                result = valueB - valueA;
            }
        });

        return result;
    });

    // Clear existing rows
    const tbody = document.querySelector("#emp-table tbody");
    tbody.innerHTML = '';

    // Append sorted rows
    sortedRows.forEach((row) => {
        tbody.appendChild(row);
    });
}


//table sorter 2
function sortRows2() {
    console.log("sortRows function called");
    const selectedSorter = document.querySelector(".table-sorter2");

    if (!selectedSorter) {
        console.log("No sortRows function ");
        return; // No sorting option selected
    }

    const col_index = selectedSorter.parentElement.getAttribute("col-index");
    const order = selectedSorter.value;

    // Find the index of the column in the currentSortOrder array
    const existingSortIndex = currentSortOrder.findIndex((sort) => sort.colIndex === col_index);
    console.log(existingSortIndex)

    if (existingSortIndex !== -1) {
        // Column already exists in the sort order, update its order
//        currentSortOrder[existingSortIndex].order = order;
         currentSortOrder=[]
        currentSortOrder.push({ colIndex: col_index, order: order });
//        console.log(order)
        console.log(currentSortOrder)
        console.log("flag 0"+ order)
    } else {
        // Column does not exist in the sort order, add it
        currentSortOrder.push({ colIndex: col_index, order: order });
        console.log(currentSortOrder)
    }

    // Apply sorting based on the current sort order
    const rows = Array.from(document.querySelectorAll("#emp-table tbody tr"));

    const sortedRows = rows.sort((a, b) => {
        let result = 0;

        currentSortOrder.forEach((sort) => {
            const valueA = parseInt(a.querySelector(`td:nth-child(${sort.colIndex})`).textContent);
            const valueB = parseInt(b.querySelector(`td:nth-child(${sort.colIndex})`).textContent);

            if (sort.order === "asc") {
                result = valueA - valueB;
            } else {
                result = valueB - valueA;
            }
        });

        return result;
    });

    // Clear existing rows
    const tbody = document.querySelector("#emp-table tbody");
    tbody.innerHTML = '';

    // Append sorted rows
    sortedRows.forEach((row) => {
        tbody.appendChild(row);
    });
}
//filter rows3
function sortRows3() {
    console.log("sortRows function called");
    const selectedSorter = document.querySelector(".table-sorter3");

    if (!selectedSorter) {
        console.log("No sortRows function ");
        return; // No sorting option selected
    }

    const col_index = selectedSorter.parentElement.getAttribute("col-index");
    const order = selectedSorter.value;

    // Find the index of the column in the currentSortOrder array
    const existingSortIndex = currentSortOrder.findIndex((sort) => sort.colIndex === col_index);
    console.log(existingSortIndex)

    if (existingSortIndex !== -1) {
        // Column already exists in the sort order, update its order
//        currentSortOrder[existingSortIndex].order = order;
         currentSortOrder=[]
        currentSortOrder.push({ colIndex: col_index, order: order });
//        console.log(order)
        console.log(currentSortOrder)
        console.log("flag 0"+ order)
    } else {
        // Column does not exist in the sort order, add it
        currentSortOrder.push({ colIndex: col_index, order: order });
        console.log(currentSortOrder)
    }

    // Apply sorting based on the current sort order
    const rows = Array.from(document.querySelectorAll("#emp-table tbody tr"));

    const sortedRows = rows.sort((a, b) => {
        let result = 0;

        currentSortOrder.forEach((sort) => {
            const valueA = parseInt(a.querySelector(`td:nth-child(${sort.colIndex})`).textContent);
            const valueB = parseInt(b.querySelector(`td:nth-child(${sort.colIndex})`).textContent);

            if (sort.order === "asc") {
                result = valueA - valueB;
            } else {
                result = valueB - valueA;
            }
        });

        return result;
    });

    // Clear existing rows
    const tbody = document.querySelector("#emp-table tbody");
    tbody.innerHTML = '';

    // Append sorted rows
    sortedRows.forEach((row) => {
        tbody.appendChild(row);
    });
}
// filter_value_dict {2 : Value selected, 4:value, 5: value}

function filter_rows() {
    allFilters = document.querySelectorAll(".table-filter")
    var filter_value_dict = {}

    allFilters.forEach((filter_i) => {
        col_index = filter_i.parentElement.getAttribute('col-index')

        value = filter_i.value
        if (value != "all") {
            filter_value_dict[col_index] = value;
        }
    });

    var col_cell_value_dict = {};

    const rows = document.querySelectorAll("#emp-table tbody tr");
    rows.forEach((row) => {
        var display_row = true;

        allFilters.forEach((filter_i) => {
            col_index = filter_i.parentElement.getAttribute('col-index')
            col_cell_value_dict[col_index] = row.querySelector("td:nth-child(" + col_index+ ")").innerHTML
        })

        for (var col_i in filter_value_dict) {
            filter_value = filter_value_dict[col_i]
            row_cell_value = col_cell_value_dict[col_i]

            if (row_cell_value.indexOf(filter_value) == -1 && filter_value != "all") {
                display_row = false;
                break;
            }


        }

        if (display_row == true) {
            row.style.display = "table-row"

        } else {
            row.style.display = "none"

        }





    })

}

function loading() {
  document.querySelectorAll(".bar").forEach(function(current) {
    let startWidth = 0;
    const endWidth = current.dataset.size;

    /*
    setInterval() time sholud be set as trasition time / 100.
    In our case, 2 seconds / 100 = 20 milliseconds.
    */
    const interval = setInterval(frame, 20);

    function frame() {
      if (startWidth >= endWidth) {
        clearInterval(interval);
      } else {
          startWidth++;
          current.style.width = `${endWidth}%`;
          current.firstElementChild.innerText = `${startWidth}%`;
        }
     }
  });
}

setTimeout(loading, 1000);
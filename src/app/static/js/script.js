window.addEventListener('DOMContentLoaded', function () {

        nameInput = document.getElementsByName("name").item(0)
        emailInput = document.getElementsByName("email").item(0)
        password = document.getElementsByName("password1").item(0)
        let passwordRepeat = document.getElementsByName("password2").item(0)
        nameInput.addEventListener('input', function () {
            if (nameInput.value == "") {
                document.querySelector(".btn").disabled = true
            } else {
                document.querySelector(".btn").disabled = false
            }
        })
        emailInput.addEventListener('input', function () {
            if (emailInput.value == "") {
                document.querySelector(".btn").disabled = true
            } else {
                document.querySelector(".btn").disabled = false
            }
        })
        password.addEventListener('input', function () {
            if (password.value == "") {
                document.querySelector(".btn").disabled = true
            } else {
                document.querySelector(".btn").disabled = false
            }
        })
        passwordRepeat.addEventListener('input', () => {
            if (password.value !== passwordRepeat.value) {
                passwordRepeat.style.borderColor = 'red'
                document.querySelector(".btn").disabled = true
            } else {
                passwordRepeat.style.borderColor = '#ced4da'
                document.querySelector(".btn").disabled = false
            }
        })
    }
)

var header;
var csrf;

$(document).ready(function () {
    header = $("meta[name='_csrf_header']").attr("content");
    csrf = $("meta[name='_csrf']").attr("content");

    $('.add-record').click(function () {
        let form = $("#add-record-form")
        let accountId = form.find('input[name="accountId"]')[0]
        let bankId = form.find('select[name="bankId"]')[0]
        let isIncome = form.find('select[name="isIncome"]')[0]
        let categoryId = form.find('select[name="categoryId"]')[0]
        let sum = form.find('input[name="sum"]')[0]
        let date = form.find('input[name="date"]')[0]
        let description = form.find('input[name="description"]')[0]

        let record = {
            "bankId": bankId.value,
            "isIncome": isIncome.value,
            "categoryId": categoryId.value,
            "sum": sum.value,
            "date": date.value,
            "description": description.value,
        }

        addRecord(accountId.value, record, header, csrf)
    })
});


function addRecord(id, record, header, csrf) {
    $.ajax({
        type: "POST",
        url: "http://localhost:8080/record/" + id,
        contentType: "application/json",
        dataType: 'json',
        data: JSON.stringify(record),
        beforeSend: function (xhr) {
            xhr.setRequestHeader(header, csrf);
        },
        success: function (response) {
            let tbody = $('#record-table').find('tbody')
            tbody.before(getFormattedRecord(response), tbody.firstChild)
        },
        error: function (msg) {
            console.log(msg);
        }
    });
}

function getFormattedRecord(response) {
    let text = ' '
    text += '<tr>' +
        '<td class="edit-icon"><a href="/edit/' + response.id + '"><i class="fas fa-edit"></i></a></td>' +
        '<td><div class="record-category">' +
        '<div class="record-icon">' +
        '<i class="fas ' + response.category.iconName + ' mr-4" style="color:' + response.category.color + '"></i>' +
        '</div>' + response.category.name + '</div></td>' +
        '<td class="record-account text-center">' + response.bank.name + '</td>' +
        '<td class="record-description text-center"></td><td class="record-sum text-center">' + response.sum + '</td>' +
        '<td class="record-date text-right">\n' + new Date(response.date) + '</td>' +
        '<td class="delete-icon"><a href="/del/' + response.id + '"><i class="fas fa-trash"></i></a></td>' +
        '</tr>'
    return text
}

function dateParse(date) {
    let d = new Date(date)
    return d.getDay() + "." + d.getMonth() + "." + d.getFullYear()
}
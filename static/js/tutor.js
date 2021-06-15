console.log('yomamama')



var favourites = document.getElementsByClassName('favStars')
console.log(favourites)

for (var i = 0; i < favourites.length; i++){
    favourites[i].addEventListener('click', function (){
        console.log('hdhbd')
        var tutorId = this.dataset.tutor
        var action = this.dataset.action
        updateFavs(tutorId, action)
    })
}

function updateFavs(tutorId, action){
    console.log('in updatefav')
    url = '/update_favourites/'

    fetch(url, {
        method : 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'tutorId': tutorId, 'action': action})
    })
        .then((response)=>{
            return response.json()
        })
        .then((data) =>{
        console.log('data: ', data)
        location.reload()
    })
}

document.querySelector.addEventListener("DOMContentLoaded", () => {
  alert("Hello World");
})


function geoFindMe() {

    const options = {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0
    };
    const status = document.querySelector('#status');
    const mapLink = document.querySelector('#map-link');
  
    mapLink.href = '';
    mapLink.textContent = '';
  
    function success(position) {
      const latitude  = position.coords.latitude;
      const longitude = position.coords.longitude;

      document.querySelector('#lon').value = longitude;
      document.querySelector('#lat').value = latitude;
      document.querySelector('#url').innerHTML = `https://www.openstreetmap.org/#map=18/${latitude}/${longitude}`;
  
      status.textContent = '';
      mapLink.href = `https://www.openstreetmap.org/#map=18/${latitude}/${longitude}`;
      mapLink.textContent = `Latitude: ${latitude} °, Longitude: ${longitude} °`;
    }
  
    function error() {
      status.textContent = 'Unable to retrieve your location';
      document.querySelector('#lon').value = 'Unable to retrieve your location';
      document.querySelector('#lat').value = 'Unable to retrieve your location';
      document.querySelector('#url').value = 'Unable to retrieve your location';
    }
  
    if (!navigator.geolocation) {
      status.textContent = 'Geolocation is not supported by your browser';
      document.querySelector('#lon').value = 'Geolocation is not supported by your browser';
      document.querySelector('#lat').value = 'Geolocation is not supported by your browser';
      document.querySelector('#url').value = 'Geolocation is not supported by your browser';
    } else {
      status.textContent = 'Locating…';
      
      navigator.geolocation.getCurrentPosition(success, error, options);
    }
  
}
  
document.querySelector('#find-me').addEventListener('click', () => {
  geoFindMe();
});


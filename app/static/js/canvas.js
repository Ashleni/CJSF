const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

function makeSVG(html){

    var data = '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">' +
      '<foreignObject width="100%" height="100%">' +
      '<div xmlns="http://www.w3.org/1999/xhtml" style="font-size:12px; border: 1px solid black">' +
      html +
      '</div>' +
      '</foreignObject>' +
      '</svg>';

    return data
    }
    
class Location {
  constructor(latitude, longitude, placeName, centerLat, centerLong) {
    this.latitude = latitude
    this.longitude = longitude
    this.centerX = 250
    this.centerY = 150
    this.placeName = placeName
    this.circleClicked = false
    this.calculateXY(centerLat, centerLong)

		this.circle = new Path2D();
    this.circle.arc(this.X, this.Y, 5, 0, 2 * Math.PI);
  }
  
  addOthers(others) {
  	this.others = others
  }
  calculateXY(centerLat, centerLong) {

  	this.X = this.centerX - 4000 * (centerLong - this.longitude)
    this.Y = this.centerY + 4000 * (centerLat - this.latitude)
  }
 
 redrawOthers() {
 	for (let i = 0; i < this.others.length; i++) {
  	this.others[i].placeCircle()
  }
 }
  

  placeCircle() {
    // Create circle
    ctx.fillStyle = 'red';
    ctx.fill(this.circle);
	}
  
  attach() {
    // Listen for mouse moves
    const placeName = this.placeName
    const X = this.X
    const Y = this.Y
    const circle = this.circle
    const redraw = this.redrawOthers
    const others = this.others
		
    const centerX = this.centerX
    const centerY = this.centerY
    canvas.addEventListener('click', function(event) {
      // Check whether point is inside circle
      var data = makeSVG(`
    <p>${placeName}</p>
    `)

      var DOMURL = window.URL || window.webkitURL || window;

      var img = new Image();
      var svg = new Blob([data], {
        type: 'image/svg+xml;charset=utf-8'
      });
      var url = DOMURL.createObjectURL(svg);

		if (ctx.isPointInPath(circle, event.offsetX, event.offsetY)) {
      if (this.circleClicked) {
        ctx.fillStyle = 'red';
      } else {
        ctx.fillStyle = 'green';

      }

      if (this.circleClicked) {
        ctx.clearRect(0, 0, 500, 300);
        for (let i = 0; i < others.length; i++) {
          others[i].placeCircle()
        }
      } else {
      	//draws the box
        img.onload = function() {
          ctx.drawImage(img, X, Y);
          DOMURL.revokeObjectURL(url);
        }
        img.src = url;
        //draws the dash	
        
        ctx.beginPath();
        ctx.setLineDash([1, 1]);
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(X, Y);
        ctx.stroke();
        ctx.closePath();
      }

      ctx.fill(circle);
      this.circleClicked = !this.circleClicked

    }});


  }
}

function initalize(centerLat, centerLong, otherLocations) {
    console.log(otherLocations)
    const center = new Location(centerLat, centerLong, "Your location", centerLat, centerLong)
    center.placeCircle()

    allCircles = []

    allCircles.push(center)

    const places = Object.keys(otherLocations)
    for (let i = 0; i < places.length; i++) {
        const location = places[i]
        const coordinates = otherLocations[location]
        console.log(coordinates)
        const place1 = new Location(coordinates[0], coordinates[1], location, centerLat, centerLong)
    place1.placeCircle()
    allCircles.push(place1)
    }

    center.attach()
    for (let i = 0; i < allCircles.length; i++) {
        const place = allCircles[i]
    place.addOthers(allCircles)
    place.attach()
    }
}
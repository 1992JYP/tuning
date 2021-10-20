
// create svg element for darwing Ball;
var svg = d3.select("#Ball").append("svg").attr("width", 300).attr("height", 300);


var cookieOptions = {
    'path': '/',
    'domain': 'localhost',
    'expires': new Date(Date.now()+ 24*60*60*1000), // it will last for a day
    'secure': false,
    'samesite': 'strict',
}

var color = 'red';
var count = 0;
if (Cookie.has('ball_color') && Cookie.has('ball_count')) {
    color = Cookie.get('ball_color');
    count = parseInt(Cookie.get('ball_count')) + 1;
    Cookie.set('ball_count', count, cookieOptions);
} else {
    // 50/50 chance of red or blue ball color
    if (Math.random() > 0.5) {
        color = 'red';
    } else {
        color = 'blue';
    }
    Cookie.set('ball_color', color, cookieOptions);
    Cookie.set('ball_count', count, cookieOptions);
}

// Add the path using this helper function
svg.append('circle')
  .attr('cx', 150)
  .attr('cy', 130)
  .attr('r', 130)
  .attr('stroke', 'black')
  .attr('fill', color);

var viewCountTag = document.getElementById("viewCount");
viewCountTag.innerHTML = count + '<small class="text-muted"> viewed</small>';

function reset() { 
    Cookie.empty();
    location.reload();
}

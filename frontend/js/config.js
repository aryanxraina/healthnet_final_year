// Backend API base URL for real server
// Update this when deploying to production
(function(){
  try {
    if (window.healthAPI) {
      window.healthAPI.baseURL = 'http://127.0.0.1:8000';
    }
  } catch (e) {}
})();



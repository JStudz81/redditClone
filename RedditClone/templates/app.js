// Define the `phonecatApp` module
var redditApp = angular.module('redditApp', []);

// Define the `PhoneListController` controller on the `phonecatApp` module
redditApp.controller('IndexController', function IndexController($scope, $http) {

    $scope.vote = function(postId) {
        $http.get("vote/" + postId);
    };

});
/**
 * Created by sid on 20/9/17.
 */
angular.module('TaskManagerApp.controllers', [])
    .controller('signupController', function ($scope, signUpService, signInService, $cookieStore, $window) {
        $scope.role = "STUDENT";
        $scope.signup = function () {
            $scope.errorMessage = "";
            var signupData = {
                "email": $scope.email,
                "first_name": $scope.firstName,
                "last_name": $scope.lastName,
                "password": $scope.password,
                "role": $scope.role
            }
            signUpService.signUp(signupData).then(function (response) {
                console.log(response)
                if (response.status == 201) {
                    $scope.signin();
                }
                else {
                    $scope.errorMessage = response.data;
                }
            })
        }
        $scope.signin = function () {
            var signinData = {
                "email": $scope.email,
                "password": $scope.password,
            }
            signInService.signIn(signinData).then(function (response) {
                if (response.status == 201) {
                    // save the auth_token in cookies
                    $cookieStore.put('auth_token', response.data.auth_token);
                    // navigate to home page
                    $window.location.href = '/home/';
                }
                else {
                    $scope.errorMessage = response.data;
                }
            })
        }
    })
    .controller('logoutController', function ($scope, $cookieStore, $window) {
        $scope.logout = function () {
            $cookieStore.remove('auth_token');
            $window.location.href = '/logout/'
        }
    })
    .controller('signinController', function ($scope, signInService, $cookieStore, $window) {
        $scope.role = "STUDENT";
        $scope.signin = function () {
            $scope.errorMessage = "";
            var signinData = {
                "email": $scope.email,
                "password": $scope.password,
            }
            signInService.signIn(signinData).then(function (response) {
                if (response.status == 201) {
                    // save the auth_token in cookies
                    $cookieStore.put('auth_token', response.data.auth_token);
                    // navigate to home page
                    $window.location.href = '/home/';
                }
                else {
                    $scope.errorMessage = response.data;
                }
            })

        }
    })
    .controller('userController', function ($scope, userService, $rootScope, $window) {
        $scope.userData = function (userId) {
            userService.userData(userId).then(function (response) {
                if (response.status == 200) {
                    // save the user data in rootscope
                    $rootScope.userData = response.data;
                }
                else {
                    $window.location.href = "/"
                    console.log(response)
                    $scope.errorMessage = response.data;
                }
            })
        }
    })
    .controller('adminController', function ($scope, userService, $rootScope, $window, $timeout) {
        $scope.getStudents = function () {
            $scope.errorMessage = "";
            $scope.students = []
            userService.listStudents().then(function (response) {
                console.log(response);
                if (response.status == 200) {
                    $scope.students = response.data;
                }
                else {
                    $scope.errorMessage = response.data;
                }
            })
        }
        $scope.getTaskList = function () {
            $scope.errorMessage = "";
            $scope.tasks = []
            userService.allTaskList().then(function (response) {
                console.log(response);
                if (response.status == 200) {
                    $scope.tasks = response.data;
                }
                else {
                    $scope.errorMessage = response.data;
                }
            })
        }
        $scope.deleteTask = function (task) {
            $scope.errorMessage = "";
            userService.taskDelete(task.id).then(function (response) {
                console.log(response);
                if (response.status == 204) {
                    $scope.getTaskList();
                }
                else {
                    $scope.errorMessage = response.data;
                }
            })
        }
        $scope.createTask = function () {
            $scope.errorMessage = "";
            console.log($scope.aStudents);
            var taskData = {
                "title": $scope.title,
                "description": $scope.description,
                "created_by": $rootScope.userData.id
            }
            userService.taskCreate(taskData).then(function (response) {
                console.log(response);
                if (response.status == 201) {
                    $scope.allotTask(response.data.id);
                }
                else {
                    $scope.errorMessage = response.data;
                }
            })
        }
        $scope.allotTask = function (task_id) {
            $scope.errorMessage = "";
            var taskData = $scope.aStudents;
            userService.allotTask(task_id, taskData).then(function (response) {
                console.log(response);
                if (response.status == 201) {
                    $scope.errorMessage = "Task Created and Allotted!"
                    // navigate to home page
                    $timeout(function () {
                        $window.location.href = '/home/';
                    }, 800)

                }
                else {
                    $scope.errorMessage = response.data;
                }
            })
        }

    })
    .controller('taskController', function ($scope, userService) {
        $scope.taskList = function () {
            $scope.errorMessage = "";
            $scope.tasks = []
            userService.taskList().then(function (response) {
                if (response.status == 200) {
                    $scope.tasks = response.data;
                }
                else {
                    $scope.errorMessage = response.data;
                }
            })

        }
        $scope.updateStatus = function (task, status) {
            task.status = status;
            userService.updateStatus(task).then(function (response) {
                if (response.status == 200) {

                }
                else {
                    $scope.errorMessage = response.data;
                }
            })

        }

    })

(function(){
    angular.module('ngLoadingSpinner', ['angularSpinner'])
    .directive('usSpinner',   ['$http', '$rootScope' ,function ($http, $rootScope){
        return {
            link: function (scope, elm, attrs)
            {
                $rootScope.spinnerActive = false;
                scope.isLoading = function () {
                    return $http.pendingRequests.length > 0;
                };

                /**
                 * Edited by Ralph:
                 *
                 * The directive overrides all controls of the angular-spinner directive
                 * and does not provide a controls to use angular-spinner feature of 2-way
                 * bound display.
                 *
                 * This is a small hack that works for our usecase. I am disabling
                 * the watcher when we have set the spinnerOn attr, on the thought that
                 * the variable on spinnerOn will handle the show/hide of the directive
                 *
                 * I have raised a issue to track the same
                 * https://github.com/adonespitogo/angular-loading-spinner/issues/9
                 */
                if(!attrs.spinnerOn) {
                    scope.$watch(scope.isLoading, function (loading)
                    {
                        $rootScope.spinnerActive = loading;
                        if(loading){
                            elm.removeClass('ng-hide');
                        }else{
                            elm.addClass('ng-hide');
                        }
                    });
                }

            }
        };

    }]);
}).call(this);

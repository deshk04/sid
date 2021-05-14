cd /sid/src/angular/ng-sid/
# npm install
if [ -d "/app/node_modules" ] 
then
    if [ -d "/sid/src/angular/ng-sid/node_modules" ]; then rm -Rf "/sid/src/angular/ng-sid/node_modules"; fi
    ln -s /app/node_modules .
else
    echo "Error: Directory /app/node_modules doesn't exits"
fi
# while true; do sleep 2; done
ng serve --port 4200 --host 0.0.0.0 --proxy-config proxy.conf.json

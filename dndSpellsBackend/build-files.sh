# build_files.sh

# we have to do ../staticfiles in vercel.json since it vercel is dumb and 
# uses dndSpellsBackend/staticfiles as the path instead of just staticfiles

pip install -r requirements.txt
python3 manage.py collectstatic --noinput
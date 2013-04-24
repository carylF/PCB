from app import pcb, db
from app.models import Part

if __name__ == '__main__':
  db.create_all()
  pcb.run(debug=True)

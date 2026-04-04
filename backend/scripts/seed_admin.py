"""
Drizzle — Seed Admin / Super Admin
===================================
Creates an admin or super_admin user document in Firestore (no Firebase Auth step).

You must already have a Firebase Auth user (Google or email). Copy their UID from
Firebase Console → Authentication.

Usage:
    python -m backend.scripts.seed_admin --uid <FIREBASE_UID> --email <EMAIL> --role super_admin
    python -m backend.scripts.seed_admin --uid <UID> --email <E> --role admin --name "Ops Admin"

Or interactively:
    python -m backend.scripts.seed_admin
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from datetime import datetime, timezone

VALID_ROLES = ("super_admin", "admin")


def seed_staff_user(uid: str, email: str, display_name: str, role: str) -> None:
    if role not in VALID_ROLES:
        raise ValueError(f"role must be one of {VALID_ROLES}")
    from backend.config.firebase import db

    now = datetime.now(timezone.utc).isoformat()
    user_doc = {
        "uid": uid,
        "email": email,
        "display_name": display_name,
        "role": role,
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    }
    db.collection("users").document(uid).set(user_doc)
    label = "Super Admin" if role == "super_admin" else "Admin"
    print(f"✅ {label} profile created in Firestore")
    print(f"   UID:   {uid}")
    print(f"   Email: {email}")
    print(f"   Role:  {role}")
    if role == "super_admin":
        print("\n   This user can promote others via POST /auth/promote or the Users page.")


def seed_super_admin(uid: str, email: str, display_name: str = "Super Admin") -> None:
    seed_staff_user(uid, email, display_name, "super_admin")


def seed_demo_admin(uid: str, email: str, display_name: str = "Admin") -> None:
    seed_staff_user(uid, email, display_name, "admin")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed admin / super_admin Firestore user profile")
    parser.add_argument("--uid", type=str, help="Firebase Auth UID")
    parser.add_argument("--email", type=str, help="Email (must match Auth user)")
    parser.add_argument("--name", type=str, default=None, help="Display name")
    parser.add_argument(
        "--role",
        choices=list(VALID_ROLES),
        default="super_admin",
        help="Firestore role (default: super_admin)",
    )
    args = parser.parse_args()

    if not args.uid or not args.email:
        print("Interactive mode:")
        args.uid = input("  Firebase UID: ").strip()
        args.email = input("  Email: ").strip()
        r = input("  Role [super_admin]: ").strip() or "super_admin"
        if r not in VALID_ROLES:
            print(f"Invalid role; use one of {VALID_ROLES}")
            sys.exit(1)
        args.role = r
        default_name = "Super Admin" if args.role == "super_admin" else "Admin"
        args.name = input(f"  Display name [{default_name}]: ").strip() or default_name
    else:
        if args.name is None:
            args.name = "Super Admin" if args.role == "super_admin" else "Admin"

    seed_staff_user(args.uid, args.email, args.name, args.role)

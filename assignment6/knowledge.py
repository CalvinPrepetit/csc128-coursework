"""
CSC-128 Assignment 6: Auto Shop Service Bot
Calvin A. Prepetit

- This file contains the approved information the bot is allowed to use.
- Each chunk covers one self-contained topic and includes an id and source.
- The policies describe a fictional auto shop created for this assignment.
"""

DOCUMENTS = [
    {
        "id": "shop_hours",
        "source": "Customer Visit Guide - Shop Hours",
        "text": (
            "Customers can visit the service desk Monday through Friday from 7:30 AM to 6:00 PM. "
            "On Saturday, the opening time is 8:00 AM and the closing time is 2:00 PM. "
            "The shop is closed on Sunday. Holiday hours may be different, so customers should call "
            "the service desk before visiting near a holiday."
        ),
    },
    {
        "id": "appointments",
        "source": "Customer Visit Guide - Appointments",
        "text": (
            "Customers can request an appointment by phone or through the shop's online request form. "
            "An appointment request is not confirmed until the service desk responds with a day and time. "
            "Walk-ins are accepted, but customers with confirmed appointments are checked in first and "
            "wait times for walk-ins may be longer."
        ),
    },
    {
        "id": "late_arrival",
        "source": "Customer Visit Guide - Late Arrivals",
        "text": (
            "A customer who expects to arrive more than 15 minutes late should call the service desk. "
            "The shop may move a late appointment to the next available opening if there is not enough "
            "time left for the scheduled inspection or service. Calling ahead does not guarantee that the "
            "original appointment time can be kept."
        ),
    },
    {
        "id": "check_in",
        "source": "Vehicle Check-In Guide",
        "text": (
            "At drop-off, customers should bring the vehicle key, current contact information, and a clear "
            "description of the problem. The customer should also bring any "
            "warning-light photos, recent repair paperwork, or maintenance records that may help the "
            "technician understand the issue."
        ),
    },
    {
        "id": "after_hours",
        "source": "Vehicle Drop-Off Guide - After-Hours Key Drop",
        "text": (
            "Customers can leave their keys after the shop closes by using the secure key-drop box. They "
            "should park only in a marked customer space, complete the envelope, place the vehicle key "
            "inside, seal the envelope, and put it through the slot. The shop does not begin work until a "
            "service advisor contacts the customer and confirms authorization."
        ),
    },
    {
        "id": "diagnostic_authorization",
        "source": "Service Policy - Diagnostic Authorization",
        "text": (
            "A diagnostic appointment allows a technician to inspect and test the vehicle so the shop can "
            "identify the next recommended step. The shop will not start extra repairs without asking the "
            "customer. A service advisor must explain the recommendation and receive the "
            "customer's approval before additional repair work begins."
        ),
    },
    {
        "id": "estimates",
        "source": "Service Policy - Estimates and Approval",
        "text": (
            "The shop provides an estimate for recommended work before the customer approves the repair. "
            "If the technician finds that the repair plan or expected total needs to change, a service "
            "advisor will contact the customer for approval before continuing. The bot cannot quote an exact "
            "price because the vehicle must be inspected first."
        ),
    },
    {
        "id": "customer_parts",
        "source": "Service Policy - Customer-Supplied Parts",
        "text": (
            "Yes, customers may bring their own replacement parts, but installation is contingent on the "
            "technician's approval. The part must match the shop's quality parts list and come from an "
            "approved supplier. Customers must ask the service desk before the appointment, and the shop "
            "may decline a part that is incorrect, damaged, used, or does not meet the repair requirements."
        ),
    },
    {
        "id": "payment_pickup",
        "source": "Customer Pickup Guide - Payment and Release",
        "text": (
            "The service desk will contact the customer when the vehicle is ready for pickup. Payment is due "
            "before the vehicle is released, and the person picking it up should have a photo ID. A customer "
            "who cannot pick up the vehicle before closing should call the service desk to arrange another "
            "pickup time."
        ),
    },
    {
        "id": "belongings",
        "source": "Vehicle Check-In Guide - Personal Belongings",
        "text": (
            "Customers should remove cash, electronics, medication, documents, and other valuable personal "
            "items before leaving a vehicle at the shop. Child seats and items that block access to the area "
            "being inspected should also be removed when possible. The shop needs clear access to complete "
            "the approved inspection or service."
        ),
    },
    {
        "id": "unsafe_vehicle",
        "source": "Safety Guide - Driving or Towing a Vehicle",
        "text": (
            "A customer whose brakes barely work or who has severe brake loss should not drive the vehicle to the shop. "
            "The same rule applies if it has heavy smoke, "
            "active fuel leakage, repeated stalling in traffic, or another condition that makes it unsafe to "
            "control. The customer should move to a safe location when possible and contact a towing provider "
            "or emergency service instead of relying on the bot to declare the vehicle safe to drive."
        ),
    },
    {
        "id": "warranty_review",
        "source": "Service Policy - Warranty Review",
        "text": (
            "A customer asking the shop to review earlier repair work should bring the original invoice and "
            "describe what changed after the repair. A service advisor must inspect the records and the "
            "vehicle before making a warranty decision. The bot cannot promise that a repair is covered or "
            "make a final warranty decision."
        ),
    },
]

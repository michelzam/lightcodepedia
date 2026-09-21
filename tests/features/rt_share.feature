Feature: 🔗 Share unlisted — a lab page gets an unlisted address
  Michel, 2026-09-20: a row in the account menu, lab builds only, key
  connected (the gate Publish to pedia uses; the lab is unlisted). It copies the page (and the files it references relatively) into
  docs/share/<id>/ of the lab, where the Pages build renders it unlisted at
  share.lightcodepedia.org. The id belongs to the page: sharing again
  refreshes the same folder and the link never changes; Unshare deletes it.
  The dialog offers the link, an iframe snippet and a QR code.

  Background:
    Given I have a clean browser page

  Scenario: The owner shares a page — link, iframe, QR, and the picture travels
    Given I am signed in with my face already cached
    And the lab's share folder is empty
    And the lab serves "docs/components/qr.md" with the document:
      """
      # QR page

      A picture: ![pic](qr_pic.png) and a [sibling](notes.md).

      An [absolute](/tutorial101) link stays.
      """
    And the lab serves the files "qr_pic.png" and "notes.md" beside it
    When I navigate to "/components/qr"
    And I wait for the page to be interactive
    And I choose Share unlisted in my account menu
    Then the share dialog says the page is not shared
    When I press Share
    Then the share dialog offers a link, an iframe and a QR code for "qr"
    And the page was copied to the share folder with "qr_pic.png" and "notes.md"

  Scenario: Sharing again refreshes the same folder, and Unshare empties it
    Given I am signed in with my face already cached
    And the lab's share folder already holds "docs/components/qr.md" under "abc123abc123"
    And the lab serves "docs/components/qr.md" with the document:
      """
      # QR page, edited

      Nothing relative here.
      """
    When I navigate to "/components/qr"
    And I wait for the page to be interactive
    And I choose Share unlisted in my account menu
    Then the share dialog offers a link, an iframe and a QR code for "abc123abc123/qr"
    And the share dialog says the page is shared
    When I press Refresh
    Then the share was refreshed in place under "abc123abc123"
    When I press Unshare
    Then the share folder "abc123abc123" was emptied

  Scenario: A key that cannot see the lab is told so, in words
    A private repository the key was not granted answers 404. Michel read
    "HTTP 404 reading docs/tutorial101/index.md" on the live lab
    (2026-09-20); the dialog now says which repo the key lacks and what to do.

    Given I am signed in with my face already cached
    And the lab's share folder is empty
    And the lab hides "docs/components/qr.md" from this key
    When I navigate to "/components/qr"
    And I wait for the page to be interactive
    And I choose Share unlisted in my account menu
    And I press Share
    Then the share dialog says the key cannot see "michelzam/lightcodelab"

  Scenario: A shared page wears the reader's chrome
    A stranger with the link must not find a door into the lab (Michel,
    2026-09-20): brand and menu lead to lightcodepedia.org, no Get started,
    no account, no page modes.

    When I navigate to "/share/000000000000/example"
    And I wait for the page to be interactive
    Then the page reads as a shared page of Lightcodepedia
